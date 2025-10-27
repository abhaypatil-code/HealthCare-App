// HealthCare App/src/components/admin/AdminOverview.tsx
import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Activity, CreditCard, DollarSign, Users, UserPlus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/utils/apiClient';
import { useAuth } from '@/contexts/AuthContext';
import { AdminUser } from '@/types';
import { Skeleton } from '../ui/skeleton';

// Define analytics data structure
interface DashboardAnalytics {
  todays_registrations: number;
  total_patients: number;
  risk_counts: {
    diabetes_high: number;
    liver_high: number;
    heart_high: number;
    mental_health_high: number;
  };
}

const AdminOverview: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const adminUser = user as AdminUser;
  
  const [analytics, setAnalytics] = useState<DashboardAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError(null);
      try {
        const { data } = await apiClient.get('/dashboard/analytics');
        setAnalytics(data.analytics);
      } catch (err) {
        setError('Failed to load dashboard data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  const StatCard = ({
    title,
    value,
    description,
    icon,
  }: {
    title: string;
    value: string | number;
    description: string;
    icon: React.ElementType;
  }) => {
    const Icon = icon;
    return (
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
          <Icon className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          {loading ? (
             <Skeleton className="h-8 w-1/2" />
          ) : (
            <div className="text-2xl font-bold">{value}</div>
          )}
          <p className="text-xs text-muted-foreground">{description}</p>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="flex flex-col gap-4">
      {/* Welcome Header */}
      <div className="flex justify-between items-center">
        <div className="grid gap-2">
          <h1 className="text-3xl font-bold tracking-tight">
            Welcome, {adminUser?.name || 'Admin'}!
          </h1>
          <p className="text-muted-foreground">
            Here's an overview of your patient registrations and risk alerts.
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => navigate('/admin/add-patient')}>
            <UserPlus className="mr-2 h-4 w-4" /> Add New Patient
          </Button>
          <Button variant="outline" onClick={() => navigate('/admin/patients')}>
            <Users className="mr-2 h-4 w-4" /> View All Patients
          </Button>
        </div>
      </div>
      
      {error && (
        <Card className="border-destructive bg-destructive/10">
          <CardHeader>
            <CardTitle className="text-destructive">Loading Error</CardTitle>
            <CardDescription className="text-destructive">{error}</CardDescription>
          </CardHeader>
        </Card>
      )}

      {/* Analytics Cards - Fulfills MVP Requirement */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Patients"
          value={loading ? '...' : (analytics?.total_patients ?? 0)}
          description="Total number of registered patients"
          icon={Users}
        />
        <StatCard
          title="Today's Registrations"
          value={loading ? '...' : (analytics?.todays_registrations ?? 0)}
          description="New patients registered today"
          icon={UserPlus}
        />
        <StatCard
          title="High Risk: Heart"
          value={loading ? '...' : (analytics?.risk_counts.heart_high ?? 0)}
          description="Patients with high heart risk"
          icon={Activity} // Placeholder icon
        />
        <StatCard
          title="High Risk: Diabetes"
          value={loading ? '...' : (analytics?.risk_counts.diabetes_high ?? 0)}
          description="Patients with high diabetes risk"
          icon={DollarSign} // Placeholder icon
        />
        {/* You can add Liver and Mental Health cards if desired */}
      </div>

      {/* Placeholder for future charts */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <p className="text-muted-foreground">
              [Future chart: Patient Registrations Over Time]
            </p>
            <Skeleton className="h-[300px] w-full" />
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>High Risk Patients</CardTitle>
            <CardDescription>
              A summary of all high-risk patients.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              [Future list: Recently identified high-risk patients]
            </p>
             <Skeleton className="h-[300px] w-full" />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminOverview;