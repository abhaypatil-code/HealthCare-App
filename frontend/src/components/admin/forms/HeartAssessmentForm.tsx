// HealthCare App/frontend/src/components/admin/forms/HeartAssessmentForm.tsx
import React, { useState, useEffect } from 'react';
import { useForm, SubmitHandler, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/utils/apiClient';
import { HeartAssessment } from '@/types';

// Schema from backend app/schemas.py
const heartSchema = z.object({
  chest_pain_type: z.coerce.number().int().min(0).max(3, "Must be 0-3"),
  resting_blood_pressure: z.coerce.number().min(0),
  cholesterol: z.coerce.number().min(0),
  fasting_blood_sugar: z.coerce.number().int().min(0).max(1), // 0 or 1
  resting_ecg: z.coerce.number().int().min(0).max(2, "Must be 0-2"),
  max_heart_rate: z.coerce.number().min(0),
  exercise_angina: z.coerce.number().int().min(0).max(1), // 0 or 1
  st_depression: z.coerce.number().min(0),
  st_slope: z.coerce.number().int().min(0).max(2, "Must be 0-2"),
});
type HeartFormValues = z.infer<typeof heartSchema>;

interface HeartFormProps {
  patientId: number;
  existingData: HeartAssessment | null | undefined;
  onFormSubmit: () => void;
}

const HeartAssessmentForm: React.FC<HeartFormProps> = ({ patientId, existingData, onFormSubmit }) => {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { register, handleSubmit, control, reset, formState: { errors } } = useForm<HeartFormValues>({
    resolver: zodResolver(heartSchema),
    defaultValues: existingData ? {
      ...existingData,
      // Ensure select values are correctly typed if needed (react-hook-form often handles this)
    } : {
      // Provide defaults for selects if no existing data
      chest_pain_type: 0,
      fasting_blood_sugar: 0,
      resting_ecg: 0,
      exercise_angina: 0,
      st_slope: 0,
    },
  });

  useEffect(() => {
     if (existingData) {
        reset({
          ...existingData,
          // Coerce select values to string if Select expects string values
          // fasting_blood_sugar: String(existingData.fasting_blood_sugar ?? 0),
          // exercise_angina: String(existingData.exercise_angina ?? 0),
        });
     } else {
        reset({
          chest_pain_type: 0,
          fasting_blood_sugar: 0,
          resting_ecg: 0,
          exercise_angina: 0,
          st_slope: 0,
        });
     }
  }, [existingData, reset]);
  
  const onSubmit: SubmitHandler<HeartFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    const toastId = toast.loading(`${existingData ? 'Updating' : 'Saving'} Heart assessment...`);
    try {
      // Ensure numeric values are sent as numbers
      const payload = {
          ...data,
          chest_pain_type: Number(data.chest_pain_type),
          fasting_blood_sugar: Number(data.fasting_blood_sugar),
          resting_ecg: Number(data.resting_ecg),
          exercise_angina: Number(data.exercise_angina),
          st_slope: Number(data.st_slope),
      };
      await apiClient.post(`/patients/${patientId}/assessments/heart`, payload);
      toast.success('Heart assessment saved!', { id: toastId });
      onFormSubmit();
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
        {/* Simple Inputs */}
        <div className="space-y-2">
          <Label htmlFor={`heart_resting_bp_${patientId}`}>Resting BP</Label>
          <Input id={`heart_resting_bp_${patientId}`} type="number" step="1" {...register('resting_blood_pressure')} />
          {errors.resting_blood_pressure && <p className="text-destructive text-sm">{errors.resting_blood_pressure.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`heart_cholesterol_${patientId}`}>Cholesterol</Label>
          <Input id={`heart_cholesterol_${patientId}`} type="number" step="1" {...register('cholesterol')} />
          {errors.cholesterol && <p className="text-destructive text-sm">{errors.cholesterol.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`heart_max_hr_${patientId}`}>Max Heart Rate</Label>
          <Input id={`heart_max_hr_${patientId}`} type="number" step="1" {...register('max_heart_rate')} />
          {errors.max_heart_rate && <p className="text-destructive text-sm">{errors.max_heart_rate.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`heart_st_depression_${patientId}`}>ST Depression</Label>
          <Input id={`heart_st_depression_${patientId}`} type="number" step="0.1" {...register('st_depression')} />
          {errors.st_depression && <p className="text-destructive text-sm">{errors.st_depression.message}</p>}
        </div>
        
        {/* Selects for Categorical Data */}
        <div className="space-y-2">
          <Label htmlFor={`heart_cp_type_${patientId}`}>Chest Pain Type</Label>
           <Controller
            name="chest_pain_type"
            control={control}
            render={({ field }) => (
              <Select onValueChange={(val) => field.onChange(Number(val))} value={String(field.value ?? 0)}>
                <SelectTrigger id={`heart_cp_type_${patientId}`}><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">0: Typical angina</SelectItem>
                  <SelectItem value="1">1: Atypical angina</SelectItem>
                  <SelectItem value="2">2: Non-anginal pain</SelectItem>
                  <SelectItem value="3">3: Asymptomatic</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
          {errors.chest_pain_type && <p className="text-destructive text-sm">{errors.chest_pain_type.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`heart_fbs_${patientId}`}>Fasting Blood Sugar {'>'} 120?</Label>
          <Controller
            name="fasting_blood_sugar"
            control={control}
            render={({ field }) => (
              <Select onValueChange={(val) => field.onChange(Number(val))} value={String(field.value ?? 0)}>
                <SelectTrigger id={`heart_fbs_${patientId}`}><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">No (&lt;= 120 mg/dl)</SelectItem>
                  <SelectItem value="1">Yes ({'>'} 120 mg/dl)</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
          {errors.fasting_blood_sugar && <p className="text-destructive text-sm">{errors.fasting_blood_sugar.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`heart_rest_ecg_${patientId}`}>Resting ECG</Label>
          <Controller
            name="resting_ecg"
            control={control}
            render={({ field }) => (
              <Select onValueChange={(val) => field.onChange(Number(val))} value={String(field.value ?? 0)}>
                <SelectTrigger id={`heart_rest_ecg_${patientId}`}><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">0: Normal</SelectItem>
                  <SelectItem value="1">1: ST-T wave abnormality</SelectItem>
                  <SelectItem value="2">2: Probable/definite LV hypertrophy</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
          {errors.resting_ecg && <p className="text-destructive text-sm">{errors.resting_ecg.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`heart_exang_${patientId}`}>Exercise Angina?</Label>
          <Controller
            name="exercise_angina"
            control={control}
            render={({ field }) => (
              <Select onValueChange={(val) => field.onChange(Number(val))} value={String(field.value ?? 0)}>
                <SelectTrigger id={`heart_exang_${patientId}`}><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">No</SelectItem>
                  <SelectItem value="1">Yes</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
          {errors.exercise_angina && <p className="text-destructive text-sm">{errors.exercise_angina.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`heart_slope_${patientId}`}>ST Slope</Label>
           <Controller
            name="st_slope"
            control={control}
            render={({ field }) => (
              <Select onValueChange={(val) => field.onChange(Number(val))} value={String(field.value ?? 0)}>
                <SelectTrigger id={`heart_slope_${patientId}`}><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">0: Upsloping</SelectItem>
                  <SelectItem value="1">1: Flat</SelectItem>
                  <SelectItem value="2">2: Downsloping</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
          {errors.st_slope && <p className="text-destructive text-sm">{errors.st_slope.message}</p>}
        </div>
      </div>
      <Button type="submit" disabled={isSubmitting} size="sm">
        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Heart Assessment
      </Button>
    </form>
  );
};
export default HeartAssessmentForm;