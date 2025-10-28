// HealthCare App/frontend/src/components/admin/forms/LiverAssessmentForm.tsx
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
import { LiverAssessment } from '@/types';

// Schema from backend app/schemas.py
const liverSchema = z.object({
  total_bilirubin: z.coerce.number().min(0),
  direct_bilirubin: z.coerce.number().min(0),
  alkaline_phosphotase: z.coerce.number().min(0),
  alamine_aminotransferase: z.coerce.number().min(0),
  aspartate_aminotransferase: z.coerce.number().min(0),
  total_proteins: z.coerce.number().min(0),
  albumin: z.coerce.number().min(0),
  globulin: z.coerce.number().min(0), // Globulin is required to calculate A/G ratio
});
type LiverFormValues = z.infer<typeof liverSchema>;

interface LiverFormProps {
  patientId: number;
  existingData: LiverAssessment | null | undefined;
  onFormSubmit: () => void;
}

const LiverAssessmentForm: React.FC<LiverFormProps> = ({ patientId, existingData, onFormSubmit }) => {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { register, handleSubmit, reset, formState: { errors } } = useForm<LiverFormValues>({
    resolver: zodResolver(liverSchema),
    defaultValues: existingData || {},
  });
  
  useEffect(() => {
    reset(existingData || {});
  }, [existingData, reset]);

  const onSubmit: SubmitHandler<LiverFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    const toastId = toast.loading(`${existingData ? 'Updating' : 'Saving'} Liver assessment...`);
    try {
      await apiClient.post(`/patients/${patientId}/assessments/liver`, data);
      toast.success('Liver assessment saved!', { id: toastId });
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
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Form Fields */}
        <div className="space-y-2">
          <Label htmlFor={`liver_total_bilirubin_${patientId}`}>Total Bilirubin</Label>
          <Input id={`liver_total_bilirubin_${patientId}`} type="number" step="0.1" {...register('total_bilirubin')} />
          {errors.total_bilirubin && <p className="text-destructive text-sm">{errors.total_bilirubin.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`liver_direct_bilirubin_${patientId}`}>Direct Bilirubin</Label>
          <Input id={`liver_direct_bilirubin_${patientId}`} type="number" step="0.1" {...register('direct_bilirubin')} />
          {errors.direct_bilirubin && <p className="text-destructive text-sm">{errors.direct_bilirubin.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`liver_alkaline_phosphotase_${patientId}`}>Alkaline Phosphotase</Label>
          <Input id={`liver_alkaline_phosphotase_${patientId}`} type="number" step="1" {...register('alkaline_phosphotase')} />
          {errors.alkaline_phosphotase && <p className="text-destructive text-sm">{errors.alkaline_phosphotase.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`liver_alamine_aminotransferase_${patientId}`}>Alamine Aminotransferase</Label>
          <Input id={`liver_alamine_aminotransferase_${patientId}`} type="number" step="1" {...register('alamine_aminotransferase')} />
          {errors.alamine_aminotransferase && <p className="text-destructive text-sm">{errors.alamine_aminotransferase.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`liver_aspartate_aminotransferase_${patientId}`}>Aspartate Aminotransferase</Label>
          <Input id={`liver_aspartate_aminotransferase_${patientId}`} type="number" step="1" {...register('aspartate_aminotransferase')} />
          {errors.aspartate_aminotransferase && <p className="text-destructive text-sm">{errors.aspartate_aminotransferase.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`liver_total_proteins_${patientId}`}>Total Proteins</Label>
          <Input id={`liver_total_proteins_${patientId}`} type="number" step="0.1" {...register('total_proteins')} />
          {errors.total_proteins && <p className="text-destructive text-sm">{errors.total_proteins.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`liver_albumin_${patientId}`}>Albumin</Label>
          <Input id={`liver_albumin_${patientId}`} type="number" step="0.1" {...register('albumin')} />
          {errors.albumin && <p className="text-destructive text-sm">{errors.albumin.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor={`liver_globulin_${patientId}`}>Globulin</Label>
          <Input id={`liver_globulin_${patientId}`} type="number" step="0.1" {...register('globulin')} />
          {errors.globulin && <p className="text-destructive text-sm">{errors.globulin.message}</p>}
        </div>
      </div>
      <Button type="submit" disabled={isSubmitting} size="sm">
        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Liver Assessment
      </Button>
    </form>
  );
};
export default LiverAssessmentForm;