// HealthCare App/frontend/src/components/admin/forms/MentalHealthAssessmentForm.tsx
import React, { useState, useEffect } from 'react';
import { useForm, SubmitHandler, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/utils/apiClient';
import { MentalHealthAssessment } from '@/types';

// Schema from backend app/schemas.py
const mentalHealthSchema = z.object({
  phq_score: z.coerce.number().int().min(0, "Min score is 0").max(27, "Max score is 27"),
  gad_score: z.coerce.number().int().min(0, "Min score is 0").max(21, "Max score is 21"),
  sleep_quality: z.coerce.number().int().min(1).max(5), // Already validated by Select
  mood_factors: z.string().max(255, "Max 255 characters").optional().nullable(),
});
type MentalFormValues = z.infer<typeof mentalHealthSchema>;

interface MentalFormProps {
  patientId: number;
  existingData: MentalHealthAssessment | null | undefined;
  onFormSubmit: () => void;
}

const MentalHealthAssessmentForm: React.FC<MentalFormProps> = ({ patientId, existingData, onFormSubmit }) => {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { register, handleSubmit, control, reset, formState: { errors } } = useForm<MentalFormValues>({
    resolver: zodResolver(mentalHealthSchema),
    defaultValues: existingData ? {
      ...existingData,
      mood_factors: existingData.mood_factors || '', // Ensure textarea doesn't get null
    } : {
      sleep_quality: 3, // Default sleep quality
      mood_factors: '',
    },
  });
  
  useEffect(() => {
     if (existingData) {
        reset({
          ...existingData,
          mood_factors: existingData.mood_factors || '',
          // Ensure sleep quality is handled correctly if it was null before
          sleep_quality: existingData.sleep_quality || 3,
        });
     } else {
        reset({ sleep_quality: 3, mood_factors: ''});
     }
  }, [existingData, reset]);

  const onSubmit: SubmitHandler<MentalFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    const toastId = toast.loading(`${existingData ? 'Updating' : 'Saving'} Mental Health assessment...`);
    try {
      const payload = {
          ...data,
          // Ensure sleep quality is a number
          sleep_quality: Number(data.sleep_quality),
          mood_factors: data.mood_factors || null // Send null if empty
      };
      await apiClient.post(`/patients/${patientId}/assessments/mental_health`, payload);
      toast.success('Mental Health assessment saved!', { id: toastId });
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
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Form Fields */}
        <div className="space-y-2">
          <Label htmlFor={`mh_phq_score_${patientId}`}>PHQ-9 Score (0-27)</Label>
          <Input id={`mh_phq_score_${patientId}`} type="number" {...register('phq_score')} />
          {errors.phq_score && <p className="text-destructive text-sm">{errors.phq_score.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`mh_gad_score_${patientId}`}>GAD-7 Score (0-21)</Label>
          <Input id={`mh_gad_score_${patientId}`} type="number" {...register('gad_score')} />
          {errors.gad_score && <p className="text-destructive text-sm">{errors.gad_score.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`mh_sleep_quality_${patientId}`}>Sleep Quality (1-5)</Label>
           <Controller
            name="sleep_quality"
            control={control}
            render={({ field }) => (
              <Select onValueChange={(val) => field.onChange(Number(val))} value={String(field.value ?? 3)}>
                <SelectTrigger id={`mh_sleep_quality_${patientId}`}><SelectValue placeholder="Select quality" /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">1 (Very Poor)</SelectItem>
                  <SelectItem value="2">2 (Poor)</SelectItem>
                  <SelectItem value="3">3 (Average)</SelectItem>
                  <SelectItem value="4">4 (Good)</SelectItem>
                  <SelectItem value="5">5 (Very Good)</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
          {errors.sleep_quality && <p className="text-destructive text-sm">{errors.sleep_quality.message}</p>}
        </div>
      </div>
      <div className="space-y-2">
        <Label htmlFor={`mh_mood_factors_${patientId}`}>Mood Factors (Optional)</Label>
        <Textarea id={`mh_mood_factors_${patientId}`} {...register('mood_factors')} placeholder="e.g., Stress at work, family issues..." />
        {errors.mood_factors && <p className="text-destructive text-sm">{errors.mood_factors.message}</p>}
      </div>
      <Button type="submit" disabled={isSubmitting} size="sm">
        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Mental Health Assessment
      </Button>
    </form>
  );
};
export default MentalHealthAssessmentForm;