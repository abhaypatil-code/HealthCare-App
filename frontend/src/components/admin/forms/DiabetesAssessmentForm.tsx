// src/components/admin/forms/DiabetesAssessmentForm.tsx
import { useState } from 'react';
import { PatientFullData } from '../../../types';
import { AssessmentFormWrapper } from './AssessmentFormWrapper';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';

interface FormProps {
  patient: PatientFullData;
  onSave: (data: PatientFullData) => void;
}

const DiabetesAssessmentForm = ({ patient, onSave }: FormProps) => {
  const [data, setData] = useState({
    pregnancies: patient.assessments.diabetes?.pregnancies || 0,
    glucose: patient.assessments.diabetes?.glucose || 0,
    blood_pressure: patient.assessments.diabetes?.blood_pressure || 0,
    skin_thickness: patient.assessments.diabetes?.skin_thickness || 0,
    insulin: patient.assessments.diabetes?.insulin || 0,
    diabetes_pedigree_function: patient.assessments.diabetes?.diabetes_pedigree_function || 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.id]: e.target.value });
  };

  return (
    <AssessmentFormWrapper
      patientId={patient.id}
      disease="diabetes"
      title="Diabetes Assessment"
      description="Enter PIMA dataset parameters."
      formData={data}
      onSave={onSave}
    >
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-2">
          <Label htmlFor="pregnancies">Pregnancies</Label>
          <Input id="pregnancies" type="number" value={data.pregnancies} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="glucose">Glucose</Label>
          <Input id="glucose" type="number" step="0.1" value={data.glucose} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="blood_pressure">Blood Pressure</Label>
          <Input id="blood_pressure" type="number" step="0.1" value={data.blood_pressure} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="skin_thickness">Skin Thickness</Label>
          <Input id="skin_thickness" type="number" step="0.1" value={data.skin_thickness} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="insulin">Insulin</Label>
          <Input id="insulin" type="number" step="0.1" value={data.insulin} onChange={handleChange} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="diabetes_pedigree_function">Diabetes Pedigree</Label>
          <Input id="diabetes_pedigree_function" type="number" step="0.01" value={data.diabetes_pedigree_function} onChange={handleChange} />
        </div>
      </div>
    </AssessmentFormWrapper>
  );
};

export default DiabetesAssessmentForm;