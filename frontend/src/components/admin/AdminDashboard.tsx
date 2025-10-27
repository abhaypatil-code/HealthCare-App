// HealthCare App/src/components/admin/AdminDashboard.tsx
import React from 'react';
import { Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Bell,
  Home,
  Users,
  UserPlus,
  PanelLeft,
  LogOut,
} from 'lucide-react';
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

import AdminOverview from './AdminOverview';
import ViewPatients from './ViewPatients';
import AddNewUser from './AddNewUser';
import PatientDetailView from './PatientDetailView'; // Will be built next
import { useAuth } from '@/contexts/AuthContext';
import { AdminUser } from '@/types';

const AdminDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const adminUser = user as AdminUser;

  // Create breadcrumbs from the current path
  const pathnames = location.pathname.split('/').filter((x) => x);
  const breadcrumbItems = pathnames.map((value, index) => {
    const to = `/${pathnames.slice(0, index + 1).join('/')}`;
    const isLast = index === pathnames.length - 1;
    const name = value.charAt(0).toUpperCase() + value.slice(1).replace(/-/g, ' ');

    return (
      <React.Fragment key={to}>
        <BreadcrumbSeparator />
        <BreadcrumbItem>
          {isLast ? (
            <BreadcrumbPage>{name}</BreadcrumbPage>
          ) : (
            <BreadcrumbLink asChild>
              <Link to={to}>{name}</Link>
            </BreadcrumbLink>
          )}
        </BreadcrumbItem>
      </React.Fragment>
    );
  });
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <TooltipProvider>
      <div className="flex min-h-screen w-full flex-col bg-muted/40">
        {/* Desktop Sidebar (Left) */}
        <aside className="fixed inset-y-0 left-0 z-10 hidden w-14 flex-col border-r bg-background sm:flex">
          <nav className="flex flex-col items-center gap-4 px-2 sm:py-5">
            <Link
              to="/admin"
              className="group flex h-9 w-9 shrink-0 items-center justify-center gap-2 rounded-full bg-primary text-lg font-semibold text-primary-foreground md:h-8 md:w-8 md:text-base"
            >
              🩺
              <span className="sr-only">MedML</span>
            </Link>
            <Tooltip>
              <TooltipTrigger asChild>
                <Link
                  to="/admin"
                  className={`flex h-9 w-9 items-center justify-center rounded-lg ${
                    location.pathname === '/admin'
                      ? 'bg-accent text-accent-foreground'
                      : 'text-muted-foreground'
                  } transition-colors hover:text-foreground md:h-8 md:w-8`}
                >
                  <Home className="h-5 w-5" />
                  <span className="sr-only">Dashboard</span>
                </Link>
              </TooltipTrigger>
              <TooltipContent side="right">Dashboard</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Link
                  to="/admin/patients"
                  className={`flex h-9 w-9 items-center justify-center rounded-lg ${
                    location.pathname.startsWith('/admin/patients')
                      ? 'bg-accent text-accent-foreground'
                      : 'text-muted-foreground'
                  } transition-colors hover:text-foreground md:h-8 md:w-8`}
                >
                  <Users className="h-5 w-5" />
                  <span className="sr-only">View Patients</span>
                </Link>
              </TooltipTrigger>
              <TooltipContent side="right">View Patients</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Link
                  to="/admin/add-patient"
                  className={`flex h-9 w-9 items-center justify-center rounded-lg ${
                    location.pathname === '/admin/add-patient'
                      ? 'bg-accent text-accent-foreground'
                      : 'text-muted-foreground'
                  } transition-colors hover:text-foreground md:h-8 md:w-8`}
                >
                  <UserPlus className="h-5 w-5" />
                  <span className="sr-only">Add New Patient</span>
                </Link>
              </TooltipTrigger>
              <TooltipContent side="right">Add New Patient</TooltipContent>
            </Tooltip>
          </nav>
          <nav className="mt-auto flex flex-col items-center gap-4 px-2 sm:py-5">
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="outline" size="icon" className="h-9 w-9 md:h-8 md:w-8" onClick={handleLogout}>
                  <LogOut className="h-5 w-5" />
                  <span className="sr-only">Logout</span>
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">Logout</TooltipContent>
            </Tooltip>
          </nav>
        </aside>

        <div className="flex flex-col sm:gap-4 sm:py-4 sm:pl-14">
          {/* Mobile Header & Desktop Header */}
          <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
            {/* Mobile Sheet Trigger (Hamburger) */}
            <Sheet>
              <SheetTrigger asChild>
                <Button size="icon" variant="outline" className="sm:hidden">
                  <PanelLeft className="h-5 w-5" />
                  <span className="sr-only">Toggle Menu</span>
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="sm:max-w-xs">
                <nav className="grid gap-6 text-lg font-medium">
                  <Link
                    to="/admin"
                    className="group flex h-10 w-10 shrink-0 items-center justify-center gap-2 rounded-full bg-primary text-lg font-semibold text-primary-foreground md:text-base"
                  >
                    🩺
                    <span className="sr-only">MedML</span>
                  </Link>
                  <Link
                    to="/admin"
                    className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                  >
                    <Home className="h-5 w-5" />
                    Dashboard
                  </Link>
                  <Link
                    to="/admin/patients"
                    className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                  >
                    <Users className="h-5 w-5" />
                    View Patients
                  </Link>
                  <Link
                    to="/admin/add-patient"
                    className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                  >
                    <UserPlus className="h-5 w-5" />
                    Add New Patient
                  </Link>
                </nav>
              </SheetContent>
            </Sheet>

            {/* Breadcrumbs */}
            <Breadcrumb className="hidden md:flex">
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbLink asChild>
                    <Link to="/admin">Admin</Link>
                  </BreadcrumbLink>
                </BreadcrumbItem>
                {breadcrumbItems}
              </BreadcrumbList>
            </Breadcrumb>

            {/* Header Right Side */}
            <div className="relative ml-auto flex-1 md:grow-0">
              {/* <Search placeholder="Search..." /> - Removed for MVP */}
            </div>
            <Button
              variant="outline"
              size="icon"
              className="ml-auto h-8 w-8"
            >
              <Bell className="h-4 w-4" />
              <span className="sr-only">Toggle notifications</span>
            </Button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="outline"
                  size="icon"
                  className="overflow-hidden rounded-full h-8 w-8"
                >
                  <span className="font-semibold">
                    {adminUser?.name?.charAt(0).toUpperCase() || 'A'}
                  </span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>
                  {adminUser?.name || 'Admin Account'}
                  <p className="text-xs font-normal text-muted-foreground">
                    {adminUser?.email}
                  </p>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>Settings</DropdownMenuItem>
                <DropdownMenuItem>Support</DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout}>Logout</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </header>

          {/* Main Content Area */}
          <main className="grid flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8">
            <Routes>
              <Route index element={<AdminOverview />} />
              <Route path="patients" element={<ViewPatients />} />
              <Route path="patients/:patientId" element={<PatientDetailView />} />
              <Route path="add-patient" element={<AddNewUser />} />
            </Routes>
          </main>
        </div>
      </div>
    </TooltipProvider>
  );
};

export default AdminDashboard;