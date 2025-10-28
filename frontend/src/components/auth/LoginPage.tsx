// HealthCare App/src/components/auth/LoginPage.tsx
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle, Loader2 } from 'lucide-react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Zod schema for Admin Login
const adminSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});
type AdminFormValues = z.infer<typeof adminSchema>;

// Zod schema for Patient Login (fulfills 14-digit ABHA ID requirement)
const patientSchema = z.object({
  abha_id: z.string().regex(/^\d{14}$/, 'ABHA ID must be 14 digits'),
  password: z.string().min(1, 'Password is required'),
});
type PatientFormValues = z.infer<typeof patientSchema>;

const LoginPage: React.FC = () => {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { adminLogin, patientLogin } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('patient'); // State to control errors

  // Admin Form Hook
  const {
    register: registerAdmin,
    handleSubmit: handleAdminSubmit,
    formState: { errors: adminErrors },
  } = useForm<AdminFormValues>({
    resolver: zodResolver(adminSchema),
  });

  // Patient Form Hook
  const {
    register: registerPatient,
    handleSubmit: handlePatientSubmit,
    formState: { errors: patientErrors },
  } = useForm<PatientFormValues>({
    resolver: zodResolver(patientSchema),
  });

  // Handle Admin Login
  const onAdminLogin: SubmitHandler<AdminFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      await adminLogin(data);
      navigate('/admin'); // Redirect to admin dashboard
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'Login failed. Please check your credentials.';
      setError(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle Patient Login
  const onPatientLogin: SubmitHandler<PatientFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      await patientLogin(data);
      navigate('/patient'); // Redirect to patient dashboard
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'Login failed. Please check your credentials.';
      setError(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const onTabChange = (value: string) => {
    setError(null); // Clear errors when switching tabs
    setIsSubmitting(false);
    setActiveTab(value);
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Tabs defaultValue="patient" className="w-[400px]" onValueChange={onTabChange}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="patient">Patient Login</TabsTrigger>
          <TabsTrigger value="admin">Admin Login</TabsTrigger>
        </TabsList>
        
        {/* Patient Login Tab */}
        <TabsContent value="patient">
          <Card>
            <form onSubmit={handlePatientSubmit(onPatientLogin)}>
              <CardHeader>
                <CardTitle>Patient Login</CardTitle>
                <CardDescription>
                  Enter your 14-digit ABHA ID and password to access your dashboard.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {error && activeTab === 'patient' && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Login Failed</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}
                <div className="space-y-2">
                  <Label htmlFor="abha_id">ABHA ID</Label>
                  <Input
                    id="abha_id"
                    placeholder="14-digit ABHA ID"
                    {...registerPatient('abha_id')}
                  />
                  {patientErrors.abha_id && (
                    <p className="text-red-500 text-sm">{patientErrors.abha_id.message}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="patient_password">Password</Label>
                  <Input
                    id="patient_password"
                    type="password"
                    {...registerPatient('password')}
                  />
                  {patientErrors.password && (
                    <p className="text-red-500 text-sm">{patientErrors.password.message}</p>
                  )}
                </div>
              </CardContent>
              <CardFooter>
                <Button type="submit" className="w-full" disabled={isSubmitting}>
                  {isSubmitting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : 'Login as Patient'}
                </Button>
              </CardFooter>
            </form>
          </Card>
        </TabsContent>

        {/* Admin Login Tab */}
        <TabsContent value="admin">
          <Card>
            <form onSubmit={handleAdminSubmit(onAdminLogin)}>
              <CardHeader>
                <CardTitle>Admin Login</CardTitle>
                <CardDescription>
                  Enter your credentials to access the admin dashboard.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {error && activeTab === 'admin' && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Login Failed</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    placeholder="admin@med.com"
                    {...registerAdmin('email')}
                  />
                  {adminErrors.email && (
                    <p className="text-red-500 text-sm">{adminErrors.email.message}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="admin_password">Password</Label>
                  <Input
                    id="admin_password"
                    type="password"
                    {...registerAdmin('password')}
                  />
                  {adminErrors.password && (
                    <p className="text-red-500 text-sm">{adminErrors.password.message}</p>
                  )}
                </div>
              </CardContent>
              <CardFooter>
                <Button type="submit" className="w-full" disabled={isSubmitting}>
                  {isSubmitting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : 'Login as Admin'}
                </Button>
              </CardFooter>
            </form>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default LoginPage;