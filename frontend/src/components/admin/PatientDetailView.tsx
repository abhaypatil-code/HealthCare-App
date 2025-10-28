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
import EditPatientModal from './EditPatientModal'; // <-- ADDED: Import Edit modal
import { toast } from 'sonner';
import usePdfDownload from '@/hooks/usePdfDownload'; // <-- FIX: Use hook

const PatientDetailView: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>();
  const [patient, setPatient] = useState<PatientUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isConsultModalOpen, setIsConsultModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false); // <-- ADDED: State for Edit modal
  const { isDownloading, downloadPdf } = usePdfDownload(); // <-- FIX: Use hook

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
    toast.info("Assessment saved.", { description: "Patient data is being refreshed..." });
    fetchPatient();
  };
  
  // Callback for when consultation is booked
  const onConsultationBooked = () => {
    setIsConsultModalOpen(false);
    toast.success("Consultation Booked", { description: "The consultation has been added to the patient's file." });
    fetchPatient(); // Refresh patient data to show new consultation
  };

  // --- ADDED: Callback for when patient is updated ---
  const onPatientUpdated = () => {
    setIsEditModalOpen(false);
    toast.success("Patient Updated", { description: "Patient details have been saved." });
    fetchPatient(); // Refresh patient data
  };

  // Handle PDF Download using the hook
  const handleDownloadReport = () => {
    if (!patient) return;
    downloadPdf(patient.id, patient.abha_id);
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
    return <div className="text-center text-muted-foreground">Patient not found.</div>;
  }

  // Determine if consultation should be enabled (e.g., if any risk is Medium/High)
  const isAtRisk = patient.risk_prediction && (
    patient.risk_prediction.diabetes_level === 'Medium' || patient.risk_prediction.diabetes_level === 'High' ||
    patient.risk_prediction.heart_level === 'Medium' || patient.risk_prediction.heart_level === 'High' ||
    patient.risk_prediction.liver_level === 'Medium' || patient.risk_prediction.liver_level === 'High' ||
    patient.risk_prediction.mental_health_level === 'Medium' || patient.risk_prediction.mental_health_level === 'High'
  );

  return (
    <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-4">
      {/* Consultation Modal */}
      <ConsultationModal
        isOpen={isConsultModalOpen}
        onClose={() => setIsConsultModalOpen(false)}
        patientId={patient.id}
        onConsultationBooked={onConsultationBooked}
      />
      {/* --- ADDED: Edit Patient Modal --- */}
      <EditPatientModal
         isOpen={isEditModalOpen}
         onClose={() => setIsEditModalOpen(false)}
         patient={patient}
         onPatientUpdated={onPatientUpdated}
      />
    
      {/* Left Column (Patient Info) */}
      <div className="grid auto-rows-min gap-4 md:col-span-1 lg:col-span-1">
        <Card>
          <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
            <div className="space-y-1">
              <CardTitle className="text-lg font-semibold">
                {patient.full_name}
              </CardTitle>
              <CardDescription>
                ABHA: ...{patient.abha_id.slice(-4)} <br/>
                {patient.age} years old, {patient.gender} <br/>
                {patient.state_name}
              </CardDescription>
            </div>
             <User className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent>
             {/* --- FIX: Enable Edit button --- */}
            <Button variant="outline" size="sm" className="w-full" onClick={() => setIsEditModalOpen(true)}>
              <Edit className="mr-2 h-4 w-4" />
              Edit Details
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
              Height: <strong>{patient.height_cm} cm</strong>
            </div>
            <div className="text-sm">
              Weight: <strong>{patient.weight_kg} kg</strong>
            </div>
            <div className="text-xl font-bold mt-1">
              BMI: {patient.bmi}
            </div>
          </CardContent>
        </Card>
        
         <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-md font-medium">Overall Risk</CardTitle>
             <CardDescription>Highest detected risk level.</CardDescription>
          </CardHeader>
          <CardContent>
            <RiskBadge prediction={patient.risk_prediction} condensed={false} /> {/* Show detailed badge here */}
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-md font-medium">Actions</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Button 
              className="w-full" 
              onClick={() => setIsConsultModalOpen(true)}
              disabled={!isAtRisk}
              title={!isAtRisk ? "Booking only available for Medium or High risk patients" : "Book a new consultation"}
            >
              <Calendar className="mr-2 h-4 w-4" />
              Book Consultation
            </Button>
            {!isAtRisk && (
              <p className="text-xs text-muted-foreground text-center -mt-1">
                (Enabled for Medium/High risk)
              </p>
            )}
            
            <Button 
              variant="outline" 
              className="w-full"
              onClick={handleDownloadReport}
              disabled={isDownloading} // <-- FIX: Use hook state
            >
              {isDownloading ? ( // <-- FIX: Use hook state
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