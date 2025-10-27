// HealthCare App/src/components/patient/OverviewTab.tsx
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { cn } from '@/components/ui/utils';
import { FileDown, Loader2 } from 'lucide-react';
import { PatientUser, LifestyleRecommendation, Consultation } from '@/types';
import RecommendationCard from './RecommendationCard';
import { saveAs } from 'file-saver';
import apiClient from '@/utils/apiClient';
import { toast } from 'sonner';

interface OverviewTabProps {
  patient: PatientUser;
  recommendations: LifestyleRecommendation[];
}

const OverviewTab: React.FC<OverviewTabProps> = ({ patient, recommendations }) => {
  const [isDownloadingPdf, setIsDownloadingPdf] = useState(false);
  
  const riskPrediction = patient.risk_prediction;
  
  // Get "general" recommendations for the overview page
  const generalRecs = recommendations.filter(r => r.category === 'general' || r.disease_type === 'general');
  
  // Get appointments
  const appointments = patient.consultations || [];

  const getRiskBadgeVariant = (level: string | null | undefined): 'default' | 'secondary' | 'destructive' | 'outline' => {
    switch (level) {
      case 'High': return 'destructive';
      case 'Medium': return 'secondary';
      case 'Low': return 'default'; // Will be styled green
      default: return 'outline';
    }
  };
  
  const getRiskBadgeClassName = (level: string | null | undefined): string => {
     switch (level) {
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low': return 'bg-green-100 text-green-800 border-green-200';
      default: return '';
    }
  }

  // Handle PDF Download
  const handleDownloadReport = async () => {
    setIsDownloadingPdf(true);
    toast.info("Generating PDF report...", { id: 'pdf-toast' });
    try {
      const reportOptions = {
        include_demographics: true,
        include_risk_summary: true,
        include_recommendations: true,
      };
      
      const response = await apiClient.post(
        `/reports/patient/${patient.id}/download`,
        reportOptions,
        { responseType: 'blob' }
      );
      
      const blob = new Blob([response.data], { type: 'application/pdf' });
      saveAs(blob, `My_Health_Report_${patient.abha_id}.pdf`);
      
      toast.success("Report downloaded", { id: 'pdf-toast' });
      
    } catch (err) {
      console.error("PDF Download Error:", err);
      toast.error("Failed to generate report", { id: 'pdf-toast' });
    } finally {
      setIsDownloadingPdf(false);
    }
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
                    <Badge 
                      variant={getRiskBadgeVariant(riskPrediction?.diabetes_level)}
                      className={getRiskBadgeClassName(riskPrediction?.diabetes_level)}
                    >
                      {riskPrediction?.diabetes_level || 'N/A'}
                    </Badge>
                  </TableCell>
                  <TableCell>{riskPrediction?.diabetes_score ? `${(riskPrediction.diabetes_score * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                  <TableCell>{patient.assessments.diabetes ? new Date(patient.assessments.diabetes.assessed_at).toLocaleDateString() : 'N/A'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">Liver Disease</TableCell>
                  <TableCell>
                    <Badge 
                      variant={getRiskBadgeVariant(riskPrediction?.liver_level)}
                      className={getRiskBadgeClassName(riskPrediction?.liver_level)}
                    >
                      {riskPrediction?.liver_level || 'N/A'}
                    </Badge>
                  </TableCell>
                  <TableCell>{riskPrediction?.liver_score ? `${(riskPrediction.liver_score * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                  <TableCell>{patient.assessments.liver ? new Date(patient.assessments.liver.assessed_at).toLocaleDateString() : 'N/A'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">Heart Disease</TableCell>
                  <TableCell>
                    <Badge 
                      variant={getRiskBadgeVariant(riskPrediction?.heart_level)}
                      className={getRiskBadgeClassName(riskPrediction?.heart_level)}
                    >
                      {riskPrediction?.heart_level || 'N/A'}
                    </Badge>
                  </TableCell>
                  <TableCell>{riskPrediction?.heart_score ? `${(riskPrediction.heart_score * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                  <TableCell>{patient.assessments.heart ? new Date(patient.assessments.heart.assessed_at).toLocaleDateString() : 'N/A'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">Mental Health</TableCell>
                  <TableCell>
                    <Badge 
                      variant={getRiskBadgeVariant(riskPrediction?.mental_health_level)}
                      className={getRiskBadgeClassName(riskPrediction?.mental_health_level)}
                    >
                      {riskPrediction?.mental_health_level || 'N/A'}
                    </Badge>
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
              disabled={isDownloadingPdf}
            >
              {isDownloadingPdf ? (
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
              Your upcoming (dummy) consultation schedule.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {appointments.length === 0 ? (
              <p className="text-sm text-muted-foreground">You have no appointments scheduled.</p>
            ) : (
              <ul className="space-y-4">
                {appointments.map((appt: Consultation) => (
                  <li key={appt.id} className="p-3 bg-muted/50 rounded-lg">
                    <div className="font-semibold">{appt.consultation_type}</div>
                    <div className="text-sm text-muted-foreground">
                      {new Date(appt.consultation_datetime).toLocaleString()}
                    </div>
                    <Badge variant="outline" className="mt-2">{appt.status}</Badge>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
        
        {generalRecs.length > 0 && (
           <Card>
            <CardHeader>
              <CardTitle>General Advice</CardTitle>
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