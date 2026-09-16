# ClassHub

A comprehensive class management web application designed specifically for undergraduate B.Tech engineering students and their institutions.

## Features

### Core Features
- **Student Information System (SIS)** - Complete student profiles, admission, and lifecycle management
- **Class Scheduling & Timetabling** - Drag-and-drop scheduler with conflict detection
- **Attendance Management** - QR code check-in, geofencing, parent notifications
- **Grading & Gradebook** - SGPA/CGPA calculation, rubrics, report cards
- **Assignment & Assessment** - Online exams, plagiarism detection, auto-grading
- **Course & Curriculum Management** - CO-PO mapping, content drip, SCORM support
- **Communication System** - In-app messaging, SMS, email, parent portal
- **Billing & Payments** - Invoice generation, online payments, scholarships
- **Reporting & Analytics** - Custom dashboards, predictive analytics
- **User Management & Roles** - RBAC, SSO, MFA
- **Mobile Access** - Responsive design, PWA support
- **Integration & API** - REST API, webhooks, third-party integrations
- **Security & Compliance** - FERPA, GDPR, encryption, audit logs
- **AI Features** - AI assistant, predictive analytics, smart search
- **Gamification** - Points, badges, leaderboards

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Redux Toolkit** for state management
- **Ant Design** for UI components
- **Tailwind CSS** for styling
- **Vite** for build tool

### Backend
- **Django 5.0** with Django REST Framework
- **PostgreSQL 15** (Docker)
- **Redis 7** for caching
- **Celery** with RabbitMQ for async tasks
- **MinIO** for file storage

### Infrastructure
- **Docker & Docker Compose** for containerization
- **Nginx** as reverse proxy
- **Prometheus & Grafana** for monitoring

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/classhub.git
   cd classhub
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the development environment**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/v1
   - API Documentation: http://localhost:8000/api/docs
   - Django Admin: http://localhost:8000/admin
   - PgAdmin: http://localhost:5050 (with tools profile)
   - Redis Commander: http://localhost:8081 (with tools profile)

## Development

### Backend Development

1. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements/development.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Run development server**
   ```bash
   python manage.py runserver
   ```

4. **Run tests**
   ```bash
   pytest
   ```

### Frontend Development

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server**
   ```bash
   npm run dev
   ```

3. **Run tests**
   ```bash
   npm test
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## Docker Services

| Service | Port | Description |
|---------|------|-------------|
| postgres | 5432 | PostgreSQL 15 database |
| redis | 6379 | Redis 7 cache |
| rabbitmq | 5672, 15672 | RabbitMQ message broker |
| minio | 9000, 9001 | MinIO object storage |
| elasticsearch | 9200 | Elasticsearch search engine |
| backend | 8000 | Django REST API |
| frontend | 3000 | React application |
| nginx | 80, 443 | Reverse proxy |
| prometheus | 9090 | Metrics collection |
| grafana | 3001 | Metrics visualization |

## API Documentation

The API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Database Schema

The database schema is documented in the PRD document (`PRD-ClassHub.md`). Key entities include:
- Users (with roles: Student, Faculty, Admin, Parent)
- Departments
- Batches
- Courses & Course Sections
- Enrollments
- Attendance Records
- Grades & Grade Components
- Assignments & Submissions
- Fee Invoices & Payments
- Messages & Announcements

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=apps
pytest --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Deployment

### Production Deployment

1. **Set production environment variables**
   ```bash
   export DJANGO_ENV=production
   export DJANGO_SECRET_KEY=your-secure-secret-key
   ```

2. **Build and start production services**
   ```bash
   docker-compose up -d
   ```

3. **Run migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Collect static files**
   ```bash
   docker-compose exec backend python manage.py collectstatic
   ```

## Environment Variables

See `.env.example` for all available environment variables.

Key variables:
- `DJANGO_SECRET_KEY` - Django secret key
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `REDIS_URL` - Redis connection URL
- `RABBITMQ_URL` - RabbitMQ connection URL

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@classhub.com or create an issue in the repository.

## Acknowledgments

- Django REST Framework
- React
- Ant Design
- Docker
- PostgreSQL
