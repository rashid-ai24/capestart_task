-- ============================================
-- ClassHub Database Initialization Script
-- PostgreSQL 15
-- ============================================

-- ============================================
-- Create Extensions
-- ============================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- Create Custom Types
-- ============================================
CREATE TYPE student_status AS ENUM (
    'active',
    'inactive',
    'graduated',
    'suspended',
    'expelled',
    'drop_out',
    'leave_of_absence'
);

CREATE TYPE attendance_status AS ENUM (
    'present',
    'absent',
    'tardy',
    'excused'
);

CREATE TYPE payment_status AS ENUM (
    'pending',
    'partial',
    'paid',
    'overdue',
    'refunded'
);

CREATE TYPE user_role AS ENUM (
    'super_admin',
    'college_admin',
    'department_hod',
    'faculty',
    'lab_assistant',
    'student',
    'parent',
    'accountant',
    'librarian'
);

-- ============================================
-- Create Indexes for Performance
-- ============================================

-- Function for full-text search
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.first_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.last_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.email, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.admission_no, '')), 'A');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Create Audit Log Table
-- ============================================
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for audit log
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_table_name ON audit_log(table_name);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);

-- ============================================
-- Create Notification Preferences Table
-- ============================================
CREATE TABLE IF NOT EXISTS notification_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT TRUE,
    push_enabled BOOLEAN DEFAULT TRUE,
    attendance_alerts BOOLEAN DEFAULT TRUE,
    grade_alerts BOOLEAN DEFAULT TRUE,
    assignment_alerts BOOLEAN DEFAULT TRUE,
    fee_alerts BOOLEAN DEFAULT TRUE,
    announcement_alerts BOOLEAN DEFAULT TRUE,
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- Create System Settings Table
-- ============================================
CREATE TABLE IF NOT EXISTS system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- Insert Default System Settings
-- ============================================
INSERT INTO system_settings (key, value, description, is_public) VALUES
('attendance_minimum', '{"percentage": 75}', 'Minimum attendance percentage required', TRUE),
('grading_scale', '{"type": "10_point", "grades": {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C+": 5, "C": 4, "F": 0}}', 'Grading scale configuration', TRUE),
('academic_year', '{"current": "2025-2026", "start_month": 7, "end_month": 6}', 'Academic year configuration', FALSE),
('semester_count', '{"total": 8}', 'Total semesters in program', TRUE),
('late_assignment_penalty', '{"per_day": 10, "max_penalty": 50}', 'Late assignment penalty configuration', TRUE),
('fee_reminder_days', '{"before_due": [7, 3, 1], "after_due": [1, 3, 7]}', 'Fee reminder schedule', FALSE),
('ai_features_enabled', '{"lesson_planning": true, "quiz_generation": true, "predictive_analytics": true}', 'AI features toggle', FALSE),
('gamification_enabled', '{"points": true, "badges": true, "leaderboards": true}', 'Gamification features toggle', FALSE)
ON CONFLICT (key) DO NOTHING;

-- ============================================
-- Create Function to Update Timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Create Function to Calculate CGPA
-- ============================================
CREATE OR REPLACE FUNCTION calculate_cgpa(student_uuid UUID)
RETURNS TABLE(
    semester INTEGER,
    sgpa DECIMAL(4,2),
    credits INTEGER,
    cumulative_credits INTEGER,
    cumulative_grade_points DECIMAL(10,2)
) AS $$
BEGIN
    RETURN QUERY
    WITH semester_grades AS (
        SELECT 
            g.semester,
            SUM(c.credits * g.grade_point) as semester_grade_points,
            SUM(c.credits) as semester_credits
        FROM grades g
        JOIN course_sections cs ON g.course_section_id = cs.id
        JOIN courses c ON cs.course_id = c.id
        WHERE g.student_id = student_uuid
        AND g.grade != 'F'
        GROUP BY g.semester
    )
    SELECT 
        sg.semester,
        CASE 
            WHEN sg.semester_credits > 0 
            THEN ROUND(sg.semester_grade_points / sg.semester_credits, 2)
            ELSE 0 
        END as sgpa,
        sg.semester_credits as credits,
        SUM(sg.semester_credits) OVER (ORDER BY sg.semester) as cumulative_credits,
        SUM(sg.semester_grade_points) OVER (ORDER BY sg.semester) as cumulative_grade_points
    FROM semester_grades sg
    ORDER BY sg.semester;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Create Function to Calculate Attendance Percentage
-- ============================================
CREATE OR REPLACE FUNCTION calculate_attendance_percentage(
    student_uuid UUID,
    course_section_id UUID
) RETURNS DECIMAL(5,2) AS $$
DECLARE
    total_classes INTEGER;
    present_classes INTEGER;
    attendance_pct DECIMAL(5,2);
BEGIN
    SELECT COUNT(*) INTO total_classes
    FROM attendance
    WHERE student_id = student_uuid
    AND course_section_id = course_section_id;
    
    SELECT COUNT(*) INTO present_classes
    FROM attendance
    WHERE student_id = student_uuid
    AND course_section_id = course_section_id
    AND status = 'present';
    
    IF total_classes = 0 THEN
        RETURN 0;
    END IF;
    
    attendance_pct := (present_classes::DECIMAL / total_classes::DECIMAL) * 100;
    RETURN ROUND(attendance_pct, 2);
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Create Function to Get At-Risk Students
-- ============================================
CREATE OR REPLACE FUNCTION get_at_risk_students(
    threshold_attendance DECIMAL DEFAULT 75.0,
    threshold_cgpa DECIMAL DEFAULT 5.0
) RETURNS TABLE(
    student_id UUID,
    admission_no VARCHAR(20),
    student_name TEXT,
    attendance_percentage DECIMAL,
    cgpa DECIMAL,
    risk_level TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH student_stats AS (
        SELECT 
            s.id as student_id,
            s.admission_no,
            s.first_name || ' ' || s.last_name as student_name,
            COALESCE(
                (SELECT calculate_attendance_percentage(s.id, cs.id)
                 FROM course_sections cs
                 LIMIT 1),
                0
            ) as attendance_pct,
            COALESCE(
                (SELECT (SUM(g.grade_point * c.credits) / SUM(c.credits))::DECIMAL(4,2)
                 FROM grades g
                 JOIN course_sections cs2 ON g.course_section_id = cs2.id
                 JOIN courses c ON cs2.course_id = c.id
                 WHERE g.student_id = s.id
                 AND g.grade != 'F'),
                0
            ) as student_cgpa
        FROM students s
        WHERE s.status = 'active'
    )
    SELECT 
        ss.student_id,
        ss.admission_no,
        ss.student_name,
        ss.attendance_pct,
        ss.student_cgpa,
        CASE 
            WHEN ss.attendance_pct < threshold_attendance AND ss.student_cgpa < threshold_cgpa 
            THEN 'HIGH'
            WHEN ss.attendance_pct < threshold_attendance OR ss.student_cgpa < threshold_cgpa 
            THEN 'MEDIUM'
            ELSE 'LOW'
        END as risk_level
    FROM student_stats ss
    WHERE ss.attendance_pct < threshold_attendance 
    OR ss.student_cgpa < threshold_cgpa
    ORDER BY 
        CASE 
            WHEN ss.attendance_pct < threshold_attendance AND ss.student_cgpa < threshold_cgpa 
            THEN 1
            ELSE 2
        END,
        ss.attendance_pct ASC;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Create Views for Common Queries
-- ============================================

-- View: Student Dashboard Summary
CREATE OR REPLACE VIEW v_student_dashboard AS
SELECT 
    s.id as student_id,
    s.admission_no,
    s.first_name || ' ' || s.last_name as student_name,
    s.email,
    d.name as department,
    b.name as batch,
    s.roll_number,
    s.status,
    (SELECT COUNT(*) FROM attendance a WHERE a.student_id = s.id AND a.status = 'present') as classes_attended,
    (SELECT COUNT(*) FROM attendance a WHERE a.student_id = s.id) as total_classes,
    CASE 
        WHEN (SELECT COUNT(*) FROM attendance a WHERE a.student_id = s.id) > 0
        THEN ROUND(
            (SELECT COUNT(*)::DECIMAL FROM attendance a WHERE a.student_id = s.id AND a.status = 'present') /
            (SELECT COUNT(*)::DECIMAL FROM attendance a WHERE a.student_id = s.id) * 100, 
            2
        )
        ELSE 0
    END as attendance_percentage
FROM students s
JOIN batches b ON s.batch_id = b.id
JOIN departments d ON b.department_id = d.id;

-- View: Course Statistics
CREATE OR REPLACE VIEW v_course_statistics AS
SELECT 
    c.id as course_id,
    c.code as course_code,
    c.title as course_title,
    c.credits,
    d.name as department,
    cs.section_name,
    f.first_name || ' ' || f.last_name as faculty_name,
    (SELECT COUNT(*) FROM enrollments e WHERE e.course_section_id = cs.id AND e.status = 'active') as enrolled_students,
    cs.max_strength,
    ROUND(
        (SELECT COUNT(*)::DECIMAL FROM enrollments e WHERE e.course_section_id = cs.id AND e.status = 'active') /
        cs.max_strength * 100, 
        2
    ) as occupancy_percentage
FROM courses c
JOIN departments d ON c.department_id = d.id
JOIN course_sections cs ON cs.course_id = c.id
JOIN faculty f ON cs.faculty_id = f.id;

-- View: Faculty Workload
CREATE OR REPLACE VIEW v_faculty_workload AS
SELECT 
    f.id as faculty_id,
    f.first_name || ' ' || f.last_name as faculty_name,
    f.email,
    d.name as department,
    COUNT(DISTINCT cs.id) as total_sections,
    SUM(c.credits) as total_credits,
    SUM(
        (SELECT COUNT(*) FROM enrollments e WHERE e.course_section_id = cs.id AND e.status = 'active')
    ) as total_students
FROM faculty f
JOIN departments d ON f.department_id = d.id
JOIN course_sections cs ON cs.faculty_id = f.id
JOIN courses c ON cs.course_id = c.id
GROUP BY f.id, f.first_name, f.last_name, f.email, d.name;

-- ============================================
-- Create Triggers for Audit Logging
-- ============================================

-- Function to log changes
CREATE OR REPLACE FUNCTION log_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (action, table_name, record_id, new_values)
        VALUES ('INSERT', TG_TABLE_NAME, NEW.id, to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (action, table_name, record_id, old_values, new_values)
        VALUES ('UPDATE', TG_TABLE_NAME, NEW.id, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (action, table_name, record_id, old_values)
        VALUES ('DELETE', TG_TABLE_NAME, OLD.id, to_jsonb(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Grant Permissions
-- ============================================
-- These will be configured based on your Django user setup
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO classhub_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO classhub_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO classhub_user;

-- ============================================
-- Create Statistics Tables
-- ============================================
CREATE TABLE IF NOT EXISTS daily_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(date, metric_name)
);

CREATE INDEX idx_daily_statistics_date ON daily_statistics(date);
CREATE INDEX idx_daily_statistics_metric ON daily_statistics(metric_name);

-- ============================================
-- Insert Sample Data (Optional - Remove in Production)
-- ============================================
-- Uncomment below to insert sample data for testing

/*
INSERT INTO departments (id, name, code, created_at, updated_at) VALUES
(uuid_generate_v4(), 'Computer Science & Engineering', 'CSE', NOW(), NOW()),
(uuid_generate_v4(), 'Electronics & Communication', 'ECE', NOW(), NOW()),
(uuid_generate_v4(), 'Mechanical Engineering', 'ME', NOW(), NOW()),
(uuid_generate_v4(), 'Civil Engineering', 'CE', NOW(), NOW()),
(uuid_generate_v4(), 'Electrical Engineering', 'EE', NOW(), NOW());
*/

-- ============================================
-- End of Initialization Script
-- ============================================
