// src/components/admin/forms/LiverAssessmentForm.tsx
import { useState } from 'react';
import { PatientFullData } from '../../../types';
import { AssessmentFormWrapper } from './AssessmentFormWrapper';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';

interface FormProps { patient: PatientFullData; onSave: (data: PatientFullData) => void; }

const LiverAssessmentForm = ({ patient, onSave }: FormProps) => {
  const [data, setData] = useState({
    total_bilirubin: patient.assessments.liver?.total_bilirubin || 0,
    direct_bilirubin: patient.assessments.liver?.direct_bilirubin || 0,
    alkaline_phosphotase: patient.assessments.liver?.alkaline_phosphotase || 0,
    alamine_aminotransferase: patient.assessments.liver?.alamine_aminotransferase || 0,
    aspartate_aminotransferase: patient.assessments.liver?.aspartate_aminotransferase || 0,
    total_proteins: patient.assessments.liver?.total_proteins || 0,
    albumin: patient.assessments.liver?.albumin || 0,
    globulin: patient.assessments.liver?.globulin || 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.id]: e.target.value });
  };

  return (
    <AssessmentFormWrapper
      patientId={patient.id}
      disease="liver"
      title="Liver Assessment"
      description="Enter ILPD parameters. A/G Ratio is auto-calculated."
      formData={data}
      onSave={onSave}
    >
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {Object.keys(data).map((key) => (
          <div className="space-y-2" key={key}>
            <Label htmlFor={key} className="capitalize">{key.replace(/_/g, ' ')}</Label>
            <Input id={key} type="number" step="0.1" value={data[key as keyof typeof data]} onChange={handleChange} />
          </div>
        ))}
      </div>
    </AssessmentFormWrapper>
  );
};

export default LiverAssessmentForm;