// HealthCare App/src/components/admin/PatientDetailView.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle, User, Activity, Edit, Calendar, FileDown, Loader2 } from 'lucide-react';
import apiClient from '@/utils/apiClient';
import { PatientUser } from '@/types';
import AssessmentDashboard from './AssessmentDashboard';
import RiskBadge from './RiskBadge';
import ConsultationModal from './ConsultationModal';
import { toast } from 'sonner';
import { saveAs } from 'file-saver'; // Import the new dependency

const PatientDetailView: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>();
  const [patient, setPatient] = useState<PatientUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDownloadingPdf, setIsDownloadingPdf] = useState(false);

  const fetchPatient = async () => {
    if (!patientId) return;
    setLoading(true);
    setError(null);
    try {
      const { data } = await apiClient.get(`/patients/${patientId}`);
      setPatient(data.patient);
    } catch (err) {
      setError('Failed to fetch patient details.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatient();
  }, [patientId]);
  
  // Callback to refresh data after an assessment is saved
  const onAssessmentUpdate = () => {
    toast.success("Assessments updated", { description: "Patient data is being refreshed." });
    fetchPatient();
  };
  
  // Callback for when consultation is booked
  const onConsultationBooked = () => {
    setIsModalOpen(false);
    toast.success("Consultation Booked", { description: "The consultation has been added to the patient's file." });
    fetchPatient(); // Refresh patient data to show new consultation
  };

  /**
   * --- NEW: Handle PDF Report Download ---
   * Fulfills MVP: "Download/share profile (selective section export to PDF)"
   */
  const handleDownloadReport = async () => {
    if (!patientId) return;
    
    setIsDownloadingPdf(true);
    toast.info("Generating PDF report...", { id: 'pdf-toast' });
    
    try {
      // 1. Define sections to include (as per MVP)
      const reportOptions = {
        include_demographics: true,
        include_risk_summary: true,
        include_recommendations: true,
      };

      // 2. Call the API
      const response = await apiClient.post(
        `/reports/patient/${patientId}/download`,
        reportOptions,
        {
          responseType: 'blob', // <-- IMPORTANT: Tell axios to expect a file blob
        }
      );

      // 3. Save the file using file-saver
      const blob = new Blob([response.data], { type: 'application/pdf' });
      saveAs(blob, `Patient_Report_${patient?.abha_id}.pdf`);
      
      toast.success("Report downloaded", { id: 'pdf-toast' });
      
    } catch (err) {
      console.error("PDF Download Error:", err);
      toast.error("Failed to generate report", { id: 'pdf-toast' });
    } finally {
      setIsDownloadingPdf(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-64 w-full" />
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
    return <div>Patient not found.</div>;
  }

  // Determine if consultation should be enabled (e.g., if any risk is Medium/High)
  const isAtRisk = patient.risk_prediction && (
    patient.risk_prediction.diabetes_level !== 'Low' ||
    patient.risk_prediction.heart_level !== 'Low' ||
    patient.risk_prediction.liver_level !== 'Low' ||
    patient.risk_prediction.mental_health_level !== 'Low'
  );

  return (
    <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-4">
      {/* Consultation Modal */}
      <ConsultationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        patientId={patient.id}
        onConsultationBooked={onConsultationBooked}
      />
    
      {/* Left Column (Patient Info) */}
      <div className="grid gap-4 md:col-span-1 lg:col-span-1">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-lg font-semibold">
              {patient.full_name}
            </CardTitle>
            <User className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-sm text-muted-foreground">
              ABHA: ...{patient.abha_id.slice(-4)}
            </div>
            <div className="text-sm text-muted-foreground">
              {patient.age} years old, {patient.gender}
            </div>
            <div className="text-sm text-muted-foreground">
              {patient.state_name}
            </div>
            <Button variant="outline" size="sm" className="mt-4 w-full" disabled>
              <Edit className="mr-2 h-4 w-4" />
              Edit Details (Not Implemented)
            </Button>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-md font-medium">Vitals</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-sm">
              <strong>Height:</strong> {patient.height_cm} cm
            </div>
            <div className="text-sm">
              <strong>Weight:</strong> {patient.weight_kg} kg
            </div>
            <div className="text-2xl font-bold">
              BMI: {patient.bmi}
            </div>
          </CardContent>
        </Card>
        
         <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-md font-medium">Overall Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <RiskBadge prediction={patient.risk_prediction} />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-md font-medium">Actions</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Button 
              className="w-full" 
              onClick={() => setIsModalOpen(true)}
              disabled={!isAtRisk}
            >
              <Calendar className="mr-2 h-4 w-4" />
              Book Consultation
            </Button>
            {!isAtRisk && (
              <p className="text-xs text-muted-foreground text-center">
                Booking enabled for Medium/High risk patients.
              </p>
            )}
            
            <Button 
              variant="outline" 
              className="w-full"
              onClick={handleDownloadReport}
              disabled={isDownloadingPdf}
            >
              {isDownloadingPdf ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <FileDown className="mr-2 h-4 w-4" />
              )}
              Download Report
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Right Column (Assessments Dashboard) */}
      <div className="md:col-span-2 lg:col-span-3">
        <AssessmentDashboard 
          patient={patient} 
          onAssessmentUpdate={onAssessmentUpdate} 
        />
      </div>
    </div>
  );
};

export default PatientDetailView;