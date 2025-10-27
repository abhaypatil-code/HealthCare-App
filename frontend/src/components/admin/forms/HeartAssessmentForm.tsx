// src/components/admin/forms/HeartAssessmentForm.tsx
import { useState } from 'react';
import { PatientFullData } from '../../../types';
import { AssessmentFormWrapper } from './AssessmentFormWrapper';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';

interface FormProps { patient: PatientFullData; onSave: (data: PatientFullData) => void; }

const HeartAssessmentForm = ({ patient, onSave }: FormProps) => {
  const [data, setData] = useState({
    chest_pain_type: patient.assessments.heart?.chest_pain_type || 0,
    resting_blood_pressure: patient.assessments.heart?.resting_blood_pressure || 0,
    cholesterol: patient.assessments.heart?.cholesterol || 0,
    fasting_blood_sugar: patient.assessments.heart?.fasting_blood_sugar || 0,
    resting_ecg: patient.assessments.heart?.resting_ecg || 0,
    max_heart_rate: patient.assessments.heart?.max_heart_rate || 0,
    exercise_angina: patient.assessments.heart?.exercise_angina || 0,
    st_depression: patient.assessments.heart?.st_depression || 0,
    st_slope: patient.assessments.heart?.st_slope || 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.id]: e.target.value });
  };
  
  const handleSelectChange = (id: keyof typeof data, value: string) => {
    setData((prev) => ({ ...prev, [id]: parseInt(value) }));
  };

  return (
    <AssessmentFormWrapper
      patientId={patient.id}
      disease="heart"
      title="Heart Assessment"
      description="Enter UCI Heart Disease parameters."
      formData={data}
      onSave={onSave}
    >
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Simple Inputs */}
        <div className="space-y-2">
          <Label htmlFor="resting_blood_pressure">Resting Blood Pressure</Label>
          <Input id="resting_blood_pressure" type="number" value={data.resting_blood_pressure} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="cholesterol">Cholesterol</Label>
          <Input id="cholesterol" type="number" value={data.cholesterol} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="max_heart_rate">Max Heart Rate</Label>
          <Input id="max_heart_rate" type="number" value={data.max_heart_rate} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="st_depression">ST Depression</Label>
          <Input id="st_depression" type="number" step="0.1" value={data.st_depression} onChange={handleChange} />
        </div>
        
        {/* Selects for Categorical Data */}
        <div className="space-y-2">
          <Label>Chest Pain Type</Label>
          <Select onValueChange={(v) => handleSelectChange('chest_pain_type', v)} value={String(data.chest_pain_type)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="0">Type 0</SelectItem><SelectItem value="1">Type 1</SelectItem>
              <SelectItem value="2">Type 2</SelectItem><SelectItem value="3">Type 3</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label>Fasting Blood Sugar {'>'} 120</Label>
          <Select onValueChange={(v) => handleSelectChange('fasting_blood_sugar', v)} value={String(data.fasting_blood_sugar)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="1">Yes</SelectItem><SelectItem value="0">No</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label>Resting ECG</Label>
          <Select onValueChange={(v) => handleSelectChange('resting_ecg', v)} value={String(data.resting_ecg)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="0">Type 0</SelectItem><SelectItem value="1">Type 1</SelectItem><SelectItem value="2">Type 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label>Exercise Angina</Label>
          <Select onValueChange={(v) => handleSelectChange('exercise_angina', v)} value={String(data.exercise_angina)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="1">Yes</SelectItem><SelectItem value="0">No</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label>ST Slope</Label>
          <Select onValueChange={(v) => handleSelectChange('st_slope', v)} value={String(data.st_slope)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="0">Type 0</SelectItem><SelectItem value="1">Type 1</SelectItem><SelectItem value="2">Type 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </AssessmentFormWrapper>
  );
};

export default HeartAssessmentForm;