// HealthCare App/frontend/src/components/admin/forms/DiabetesAssessmentForm.tsx
import React, { useState, useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/utils/apiClient';
import { DiabetesAssessment } from '@/types';

// Schema from backend app/schemas.py
const diabetesSchema = z.object({
  pregnancies: z.coerce.number().int().min(0),
  glucose: z.coerce.number().min(0),
  blood_pressure: z.coerce.number().min(0),
  skin_thickness: z.coerce.number().min(0),
  insulin: z.coerce.number().min(0),
  diabetes_pedigree_function: z.coerce.number().min(0),
});
type FormValues = z.infer<typeof diabetesSchema>;

interface FormProps {
  patientId: number;
  existingData: DiabetesAssessment | null | undefined;
  onFormSubmit: () => void;
}

const DiabetesAssessmentForm: React.FC<FormProps> = ({ patientId, existingData, onFormSubmit }) => {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(diabetesSchema),
    defaultValues: existingData || {},
  });
  
  // Reset form if existingData changes (e.g., after save and refresh)
  useEffect(() => {
    reset(existingData || {});
  }, [existingData, reset]);

  const onSubmit: SubmitHandler<FormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    const toastId = toast.loading(`${existingData ? 'Updating' : 'Saving'} Diabetes assessment...`);
    try {
      await apiClient.post(`/patients/${patientId}/assessments/diabetes`, data);
      toast.success('Diabetes assessment saved!', { id: toastId });
      onFormSubmit(); // Trigger parent refresh
    } catch (err: any) {
      const msg = err.response?.data?.error || 'Failed to save assessment.';
      setError(msg);
      toast.error('Save failed', { id: toastId, description: msg });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 bg-muted/50 rounded-lg space-y-4 border">
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {/* Form Fields */}
        <div className="space-y-2">
          <Label htmlFor={`diabetes_pregnancies_${patientId}`}>Pregnancies</Label>
          <Input id={`diabetes_pregnancies_${patientId}`} type="number" {...register('pregnancies')} />
          {errors.pregnancies && <p className="text-destructive text-sm">{errors.pregnancies.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`diabetes_glucose_${patientId}`}>Glucose</Label>
          <Input id={`diabetes_glucose_${patientId}`} type="number" step="0.1" {...register('glucose')} />
          {errors.glucose && <p className="text-destructive text-sm">{errors.glucose.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`diabetes_blood_pressure_${patientId}`}>Blood Pressure</Label>
          <Input id={`diabetes_blood_pressure_${patientId}`} type="number" step="0.1" {...register('blood_pressure')} />
          {errors.blood_pressure && <p className="text-destructive text-sm">{errors.blood_pressure.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`diabetes_skin_thickness_${patientId}`}>Skin Thickness</Label>
          <Input id={`diabetes_skin_thickness_${patientId}`} type="number" step="0.1" {...register('skin_thickness')} />
          {errors.skin_thickness && <p className="text-destructive text-sm">{errors.skin_thickness.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`diabetes_insulin_${patientId}`}>Insulin</Label>
          <Input id={`diabetes_insulin_${patientId}`} type="number" step="0.1" {...register('insulin')} />
          {errors.insulin && <p className="text-destructive text-sm">{errors.insulin.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`diabetes_pedigree_function_${patientId}`}>Diabetes Pedigree Fn</Label>
          <Input id={`diabetes_pedigree_function_${patientId}`} type="number" step="0.001" {...register('diabetes_pedigree_function')} />
          {errors.diabetes_pedigree_function && <p className="text-destructive text-sm">{errors.diabetes_pedigree_function.message}</p>}
        </div>
      </div>
      <Button type="submit" disabled={isSubmitting} size="sm">
        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Diabetes Assessment
      </Button>
    </form>
  );
};
export default DiabetesAssessmentForm;