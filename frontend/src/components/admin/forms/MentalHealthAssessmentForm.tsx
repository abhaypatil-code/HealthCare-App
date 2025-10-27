// src/components/admin/forms/MentalHealthAssessmentForm.tsx
import { useState } from 'react';
import { PatientFullData } from '../../../types';
import { AssessmentFormWrapper } from './AssessmentFormWrapper';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Slider } from '../../ui/slider';
import { Textarea } from '../../ui/textarea';

interface FormProps { patient: PatientFullData; onSave: (data: PatientFullData) => void; }

const MentalHealthAssessmentForm = ({ patient, onSave }: FormProps) => {
  const [data, setData] = useState({
    phq_score: patient.assessments.mental_health?.phq_score || 0,
    gad_score: patient.assessments.mental_health?.gad_score || 0,
    sleep_quality: patient.assessments.mental_health?.sleep_quality || 1,
    mood_factors: patient.assessments.mental_health?.mood_factors || '',
  });

  return (
    <AssessmentFormWrapper
      patientId={patient.id}
      disease="mental_health"
      title="Mental Health Assessment"
      description="Enter PHQ-9, GAD-7, and sleep scores."
      formData={data}
      onSave={onSave}
    >
      <div className="space-y-6">
        <div className="space-y-3">
          <Label htmlFor="phq_score">PHQ-9 Score (0-27)</Label>
          <div className="flex items-center gap-4">
            <Slider
              id="phq_score"
              min={0} max={27} step={1}
              value={[data.phq_score]}
              onValueChange={(v) => setData(d => ({...d, phq_score: v[0]}))}
            />
            <Input
              type="number" className="w-20"
              value={data.phq_score}
              onChange={(e) => setData(d => ({...d, phq_score: parseInt(e.target.value)}))}
            />
          </div>
        </div>
        
        <div className="space-y-3">
          <Label htmlFor="gad_score">GAD-7 Score (0-21)</Label>
           <div className="flex items-center gap-4">
            <Slider
              id="gad_score"
              min={0} max={21} step={1}
              value={[data.gad_score]}
              onValueChange={(v) => setData(d => ({...d, gad_score: v[0]}))}
            />
            <Input
              type="number" className="w-20"
              value={data.gad_score}
              onChange={(e) => setData(d => ({...d, gad_score: parseInt(e.target.value)}))}
            />
          </div>
        </div>
        
        <div className="space-y-3">
          <Label htmlFor="sleep_quality">Sleep Quality (1-5)</Label>
           <div className="flex items-center gap-4">
            <Slider
              id="sleep_quality"
              min={1} max={5} step={1}
              value={[data.sleep_quality]}
              onValueChange={(v) => setData(d => ({...d, sleep_quality: v[0]}))}
            />
            <Input
              type="number" className="w-20"
              value={data.sleep_quality}
              onChange={(e) => setData(d => ({...d, sleep_quality: parseInt(e.target.value)}))}
            />
          </div>
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="mood_factors">Observed Mood Factors (Optional)</Label>
          <Textarea
            id="mood_factors"
            placeholder="e.g., patient reported high stress from work..."
            value={data.mood_factors}
            onChange={(e) => setData(d => ({...d, mood_factors: e.target.value}))}
          />
        </div>
      </div>
    </AssessmentFormWrapper>
  );
};

export default MentalHealthAssessmentForm;