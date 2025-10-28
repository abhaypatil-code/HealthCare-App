// HealthCare App/src/components/patient/OverviewTab.tsx
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { FileDown, Loader2 } from 'lucide-react';
import { PatientUser, LifestyleRecommendation, Consultation } from '@/types';
import RecommendationCard from './RecommendationCard';
import RiskBadge from '../admin/RiskBadge'; // <-- FIX: Use RiskBadge component
import usePdfDownload from '@/hooks/usePdfDownload'; // <-- FIX: Use hook

interface OverviewTabProps {
  patient: PatientUser;
  recommendations: LifestyleRecommendation[];
}

const OverviewTab: React.FC<OverviewTabProps> = ({ patient, recommendations }) => {
  const { isDownloading, downloadPdf } = usePdfDownload(); // <-- FIX: Use hook

  const riskPrediction = patient.risk_prediction;
  
  // Get "general" recommendations for the overview page
  const generalRecs = recommendations.filter(r => r.category === 'general' || r.disease_type === 'general');
  
  // Get appointments
  const appointments = patient.consultations || [];

  // Handle PDF Download using the hook
  const handleDownloadReport = () => {
    downloadPdf(patient.id, patient.abha_id);
  };

  return (
    <div className="grid gap-6 md:grid-cols-3">
      {/* Left Column: Vitals & Risk */}
      <div className="md:col-span-2 space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Health Profile</CardTitle>
            <CardDescription>
              Your personal health information and vital signs.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              <div className="p-4 bg-muted/50 rounded-lg">
                <div className="text-sm text-muted-foreground">Height</div>
                <div className="text-2xl font-bold">{patient.height_cm} <span className="text-base font-normal">cm</span></div>
              </div>
               <div className="p-4 bg-muted/50 rounded-lg">
                <div className="text-sm text-muted-foreground">Weight</div>
                <div className="text-2xl font-bold">{patient.weight_kg} <span className="text-base font-normal">kg</span></div>
              </div>
               <div className="p-4 bg-muted/50 rounded-lg">
                <div className="text-sm text-muted-foreground">BMI</div>
                <div className="text-2xl font-bold">{patient.bmi}</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Disease Risk Summary</CardTitle>
            <CardDescription>
              Your color-coded risk levels based on your health assessments.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Condition</TableHead>
                  <TableHead>Risk Level</TableHead>
                  <TableHead>Prediction Score</TableHead>
                  <TableHead>Last Assessed</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell className="font-medium">Diabetes</TableCell>
                  <TableCell>
                    {/* --- FIX: Use RiskBadge --- */}
                    <RiskBadge prediction={{ ...riskPrediction, diabetes_level: riskPrediction?.diabetes_level } as any} condensed={true} />
                  </TableCell>
                  <TableCell>{riskPrediction?.diabetes_score ? `${(riskPrediction.diabetes_score * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                  <TableCell>{patient.assessments.diabetes ? new Date(patient.assessments.diabetes.assessed_at).toLocaleDateString() : 'N/A'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">Liver Disease</TableCell>
                  <TableCell>
                     {/* --- FIX: Use RiskBadge --- */}
                     <RiskBadge prediction={{ ...riskPrediction, liver_level: riskPrediction?.liver_level } as any} condensed={true} />
                  </TableCell>
                  <TableCell>{riskPrediction?.liver_score ? `${(riskPrediction.liver_score * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                  <TableCell>{patient.assessments.liver ? new Date(patient.assessments.liver.assessed_at).toLocaleDateString() : 'N/A'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">Heart Disease</TableCell>
                  <TableCell>
                    {/* --- FIX: Use RiskBadge --- */}
                    <RiskBadge prediction={{ ...riskPrediction, heart_level: riskPrediction?.heart_level } as any} condensed={true} />
                  </TableCell>
                  <TableCell>{riskPrediction?.heart_score ? `${(riskPrediction.heart_score * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                  <TableCell>{patient.assessments.heart ? new Date(patient.assessments.heart.assessed_at).toLocaleDateString() : 'N/A'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">Mental Health</TableCell>
                  <TableCell>
                    {/* --- FIX: Use RiskBadge --- */}
                     <RiskBadge prediction={{ ...riskPrediction, mental_health_level: riskPrediction?.mental_health_level } as any} condensed={true} />
                  </TableCell>
                  <TableCell>{riskPrediction?.mental_health_score ? `${(riskPrediction.mental_health_score * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                  <TableCell>{patient.assessments.mental_health ? new Date(patient.assessments.mental_health.assessed_at).toLocaleDateString() : 'N/A'}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* Right Column: Appointments & Actions */}
      <div className="md:col-span-1 space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <Button 
              className="w-full" 
              onClick={handleDownloadReport}
              disabled={isDownloading} // <-- FIX: Use hook state
            >
              {isDownloading ? ( // <-- FIX: Use hook state
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <FileDown className="mr-2 h-4 w-4" />
              )}
              Download My Report (PDF)
            </Button>
          </CardContent>
        </Card>
      
        <Card>
          <CardHeader>
            <CardTitle>My Appointments</CardTitle>
            <CardDescription>
              Your upcoming consultation schedule.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {appointments.length === 0 ? (
              <p className="text-sm text-muted-foreground">You have no appointments scheduled.</p>
            ) : (
              <ul className="space-y-4">
                {appointments.slice(0, 3).map((appt: Consultation) => ( // Show max 3
                  <li key={appt.id} className="p-3 bg-muted/50 rounded-lg border">
                    <div className="font-semibold">{appt.consultation_type}</div>
                    <div className="text-sm text-muted-foreground">
                      {new Date(appt.consultation_datetime).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })}
                    </div>
                    <Badge variant={appt.status === 'Booked' ? 'secondary' : 'outline'} className="mt-1">{appt.status}</Badge>
                     {appt.notes && <p className="text-xs text-muted-foreground mt-1 truncate">Notes: {appt.notes}</p>}
                  </li>
                ))}
                 {appointments.length > 3 && <p className="text-xs text-muted-foreground mt-2">...</p>}
              </ul>
            )}
          </CardContent>
        </Card>
        
        {generalRecs.length > 0 && (
           <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-md font-medium">General Advice</CardTitle>
            </CardHeader>
            <CardContent>
              <RecommendationCard recommendation={generalRecs[0]} />
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default OverviewTab;