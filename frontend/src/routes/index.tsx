import type { RouteObject } from 'react-router-dom'
import ProfilePage from '../pages/ProfilePage.tsx'
import LandingPage from '../pages/LandingPage.tsx'
import LoginPage from '../pages/LoginPage.tsx'
import RegistrationPage from '../pages/RegistrationPage.tsx'
import VerifyEmailPage from '../pages/VerifyEmailPage.tsx'
import DashboardPage from '../pages/DashboardPage.tsx'
import NotFoundPage from '../pages/NotFoundPage.tsx'

const publicRoutes: RouteObject[] = [
  {path: '/', element: <LandingPage />},
  {path: '/login', element: <LoginPage />},
  {path: '/register', element: <RegistrationPage />},
  {path: '/verify', element: <VerifyEmailPage />}
]

const protectedRoutes: RouteObject[] = [
  {path: '/dashboard', element: <DashboardPage />}, // Needs Auth Wrapper
  {path: '/profile', element: <ProfilePage />} // Needs Auth Wrapper
]

const routes: RouteObject[] = [
  ...publicRoutes,
  ...protectedRoutes,
  {path: '*', element: <NotFoundPage />},
]

export default routes