// HealthCare App/src/components/admin/AssessmentDashboard.tsx
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle2, AlertCircle, PlusCircle, Edit } from 'lucide-react';
import { PatientUser } from '@/types';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

// Import all assessment forms
import DiabetesAssessmentForm from './forms/DiabetesAssessmentForm';
import LiverAssessmentForm from './forms/LiverAssessmentForm';
import HeartAssessmentForm from './forms/HeartAssessmentForm';
import MentalHealthAssessmentForm from './forms/MentalHealthAssessmentForm';

interface AssessmentDashboardProps {
  patient: PatientUser;
  onAssessmentUpdate: () => void; // Callback to refresh patient data
}

type AssessmentKey = 'diabetes' | 'liver' | 'heart' | 'mental_health';

const AssessmentDashboard: React.FC<AssessmentDashboardProps> = ({ patient, onAssessmentUpdate }) => {
  const { assessments } = patient;

  const assessmentConfig = [
    {
      key: 'diabetes' as AssessmentKey,
      title: 'Diabetes Assessment',
      description: 'Pregnancies, Glucose, Blood Pressure, etc.',
      component: DiabetesAssessmentForm,
      data: assessments.diabetes,
    },
    {
      key: 'liver' as AssessmentKey,
      title: 'Liver Disease Assessment',
      description: 'Bilirubin, Alkaline Phosphotase, Albumin, etc.',
      component: LiverAssessmentForm,
      data: assessments.liver,
    },
    {
      key: 'heart' as AssessmentKey,
      title: 'Heart Disease Assessment',
      description: 'Chest Pain Type, Cholesterol, Fasting Blood Sugar, etc.',
      component: HeartAssessmentForm,
      data: assessments.heart,
    },
    {
      key: 'mental_health' as AssessmentKey,
      title: 'Mental Health Assessment',
      description: 'PHQ-9, GAD-7, Sleep Quality, etc.',
      component: MentalHealthAssessmentForm,
      data: assessments.mental_health,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Patient Assessments (Step 2)</CardTitle>
        <CardDescription>
          Complete all 4 assessments to generate the patient's risk profile.
          Saving an assessment automatically triggers the ML prediction.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible className="w-full">
          {assessmentConfig.map((config) => {
            const isComplete = !!config.data;
            const FormComponent = config.component;

            return (
              <AccordionItem value={config.key} key={config.key}>
                <AccordionTrigger className="text-lg">
                  <div className="flex items-center gap-4">
                    {isComplete ? (
                      <CheckCircle2 className="h-6 w-6 text-green-500" />
                    ) : (
                      <AlertCircle className="h-6 w-6 text-yellow-500" />
                    )}
                    <div>
                      {config.title}
                      <p className="text-sm text-muted-foreground font-normal">
                        {config.description}
                      </p>
                    </div>
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                  <FormComponent
                    patientId={patient.id}
                    existingData={config.data}
                    onFormSubmit={onAssessmentUpdate} // This refreshes the parent
                  />
                </AccordionContent>
              </AccordionItem>
            );
          })}
        </Accordion>
      </CardContent>
    </Card>
  );
};

export default AssessmentDashboard;