// HealthCare App/src/components/patient/PatientDashboard.tsx
import React, { useEffect, useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import OverviewTab from './OverviewTab';
import DiseaseTab from './DiseaseTab';
import { useAuth } from '@/contexts/AuthContext';
import { PatientUser, LifestyleRecommendation } from '@/types';
import apiClient from '@/utils/apiClient';
import { Skeleton } from '../ui/skeleton';
import { Alert, AlertDescription, AlertTitle } from '../ui/alert';
import { AlertCircle, Heart, Activity, Brain, ShieldHalf } from 'lucide-react';

const PatientDashboard: React.FC = () => {
  // 1. Get Patient Data from AuthContext (fetched on login via /auth/me)
  const { user, loading: authLoading } = useAuth();
  const patient = user as PatientUser;

  // 2. State for Recommendations
  const [recommendations, setRecommendations] = useState<LifestyleRecommendation[]>([]);
  const [loadingRecs, setLoadingRecs] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 3. Fetch Recommendations
  useEffect(() => {
    if (patient) {
      const fetchRecommendations = async () => {
        setLoadingRecs(true);
        setError(null);
        try {
          // No patient_id needed, endpoint uses JWT identity
          const { data } = await apiClient.get('/recommendations');
          setRecommendations(data.recommendations);
        } catch (err) {
          setError('Failed to load lifestyle recommendations.');
          console.error(err);
        } finally {
          setLoadingRecs(false);
        }
      };
      fetchRecommendations();
    }
  }, [patient]); // Re-fetch if patient data changes

  const isLoading = authLoading || loadingRecs;

  if (isLoading && !patient) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-1/3" />
        <Skeleton className="h-48 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (!patient) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>Could not load patient data. Please try logging in again.</AlertDescription>
      </Alert>
    );
  }

  return (
    <Tabs defaultValue="overview" className="w-full">
      <TabsList className="grid w-full grid-cols-5">
        <TabsTrigger value="overview">
          <Activity className="mr-2 h-4 w-4" />
          Overview
        </TabsTrigger>
        <TabsTrigger value="diabetes">
          <ShieldHalf className="mr-2 h-4 w-4" />
          Diabetes
        </TabsTrigger>
        <TabsTrigger value="liver">
          <ShieldHalf className="mr-2 h-4 w-4" />
          Liver
        </TabsTrigger>
        <TabsTrigger value="heart">
          <Heart className="mr-2 h-4 w-4" />
          Heart
        </TabsTrigger>
        <TabsTrigger value="mental_health">
          <Brain className="mr-2 h-4 w-4" />
          Mental Health
        </TabsT>
      </TabsList>
      
      {/* Overview Tab */}
      <TabsContent value="overview">
        <OverviewTab 
          patient={patient} 
          recommendations={recommendations} 
        />
      </TabsContent>
      
      {/* Disease-Specific Tabs */}
      <TabsContent value="diabetes">
        <DiseaseTab
          title="Diabetes Risk"
          riskLevel={patient.risk_prediction?.diabetes_level}
          riskScore={patient.risk_prediction?.diabetes_score}
          recommendations={recommendations.filter(r => r.disease_type === 'diabetes')}
          assessmentData={patient.assessments.diabetes}
        />
      </TabsContent>
      
      <TabsContent value="liver">
         <DiseaseTab
          title="Liver Health"
          riskLevel={patient.risk_prediction?.liver_level}
          riskScore={patient.risk_prediction?.liver_score}
          recommendations={recommendations.filter(r => r.disease_type === 'liver')}
          assessmentData={patient.assessments.liver}
        />
      </TabsContent>
      
      <TabsContent value="heart">
         <DiseaseTab
          title="Heart Health"
          riskLevel={patient.risk_prediction?.heart_level}
          riskScore={patient.risk_prediction?.heart_score}
          recommendations={recommendations.filter(r => r.disease_type === 'heart')}
          assessmentData={patient.assessments.heart}
        />
      </TabsContent>
      
      <TabsContent value="mental_health">
         <DiseaseTab
          title="Mental Wellness"
          riskLevel={patient.risk_prediction?.mental_health_level}
          riskScore={patient.risk_prediction?.mental_health_score}
          recommendations={recommendations.filter(r => r.disease_type === 'mental_health')}
          assessmentData={patient.assessments.mental_health}
        />
      </TabsContent>
    </Tabs>
  );
};

export default PatientDashboard;