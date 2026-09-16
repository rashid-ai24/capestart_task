import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import authReducer from '../features/auth/authSlice';
import studentsReducer from '../features/students/studentsSlice';
import coursesReducer from '../features/courses/coursesSlice';
import attendanceReducer from '../features/attendance/attendanceSlice';
import gradesReducer from '../features/grades/gradesSlice';
import assignmentsReducer from '../features/assignments/assignmentsSlice';
import feesReducer from '../features/fees/feesSlice';
import messagesReducer from '../features/messages/messagesSlice';
import reportsReducer from '../features/reports/reportsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    students: studentsReducer,
    courses: coursesReducer,
    attendance: attendanceReducer,
    grades: gradesReducer,
    assignments: assignmentsReducer,
    fees: feesReducer,
    messages: messagesReducer,
    reports: reportsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
