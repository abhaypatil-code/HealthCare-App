// HealthCare App/src/components/admin/forms/AssessmentFormWrapper.tsx
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/utils/apiClient';

interface AssessmentFormWrapperProps {
  patientId: number;
  assessmentType: 'diabetes' | 'liver' | 'heart' | 'mental_health';
  validationSchema: any; // Zod schema
  transformData?: (data: any) => any; // Optional data transformer
  onFormSubmit: () => void;
  children: (
    handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void,
    register: any,
    control: any,
    errors: any
  ) => React.ReactNode;
  useFormHook: any; // e.g., useForm
  defaultValues: any;
}

/**
 * A reusable wrapper to handle API logic for all assessment forms.
 * This component is not currently used in this batch, but is a good
 * practice for refactoring. For now, logic is duplicated in each form
 * for clarity.
 *
 * --- THIS FILE IS A STUB FOR FUTURE REFACTORING ---
 * --- IT IS NOT USED IN BATCH 7 ---
 */
const AssessmentFormWrapper: React.FC<AssessmentFormWrapperProps> = () => {
  return <div>Stub</div>;
};
// We will instead implement the logic directly in each form for simplicity.

/* --- START: Individual Assessment Forms --- */

// HealthCare App/src/components/admin/forms/DiabetesAssessmentForm.tsx
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
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
  
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(diabetesSchema),
    defaultValues: existingData || {},
  });
  
  const onSubmit: SubmitHandler<FormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.post(`/patients/${patientId}/assessments/diabetes`, data);
      toast.success('Diabetes assessment saved!');
      onFormSubmit();
    } catch (err: any) {
      const msg = err.response?.data?.error || 'Failed to save assessment.';
      setError(msg);
      toast.error('Save failed', { description: msg });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 bg-muted/50 rounded-lg space-y-4">
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
          <Label htmlFor="pregnancies">Pregnancies</Label>
          <Input id="pregnancies" type="number" {...register('pregnancies')} />
          {errors.pregnancies && <p className="text-red-500 text-sm">{errors.pregnancies.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="glucose">Glucose</Label>
          <Input id="glucose" type="number" step="0.1" {...register('glucose')} />
          {errors.glucose && <p className="text-red-500 text-sm">{errors.glucose.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="blood_pressure">Blood Pressure</Label>
          <Input id="blood_pressure" type="number" step="0.1" {...register('blood_pressure')} />
          {errors.blood_pressure && <p className="text-red-500 text-sm">{errors.blood_pressure.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="skin_thickness">Skin Thickness</Label>
          <Input id="skin_thickness" type="number" step="0.1" {...register('skin_thickness')} />
          {errors.skin_thickness && <p className="text-red-500 text-sm">{errors.skin_thickness.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="insulin">Insulin</Label>
          <Input id="insulin" type="number" step="0.1" {...register('insulin')} />
          {errors.insulin && <p className="text-red-500 text-sm">{errors.insulin.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="diabetes_pedigree_function">Diabetes Pedigree Fn</Label>
          <Input id="diabetes_pedigree_function" type="number" step="0.001" {...register('diabetes_pedigree_function')} />
          {errors.diabetes_pedigree_function && <p className="text-red-500 text-sm">{errors.diabetes_pedigree_function.message}</p>}
        </div>
      </div>
      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Diabetes Assessment
      </Button>
    </form>
  );
};
export default DiabetesAssessmentForm;

// HealthCare App/src/components/admin/forms/LiverAssessmentForm.tsx
import { useForm as useLiverForm, SubmitHandler as LiverSubmitHandler } from 'react-hook-form';
import { zodResolver as zodLiverResolver } from '@hookform/resolvers/zod';
import { z as zLiver } from 'zod';
import { Input as InputLiver } from '@/components/ui/input';
import { Label as LabelLiver } from '@/components/ui/label';
import { LiverAssessment } from '@/types';
import { useState as useStateLiver } from 'react';
import apiClient from '@/utils/apiClient';
import { toast as toastLiver } from 'sonner';
import { Alert as AlertLiver, AlertDescription as AlertDescriptionLiver, AlertTitle as AlertTitleLiver } from '@/components/ui/alert';
import { Button as ButtonLiver } from '@/components/ui/button';
import { Loader2 as Loader2Liver, AlertCircle as AlertCircleLiver } from 'lucide-react';

// Schema from backend app/schemas.py
const liverSchema = zLiver.object({
  total_bilirubin: zLiver.coerce.number().min(0),
  direct_bilirubin: zLiver.coerce.number().min(0),
  alkaline_phosphotase: zLiver.coerce.number().min(0),
  alamine_aminotransferase: zLiver.coerce.number().min(0),
  aspartate_aminotransferase: zLiver.coerce.number().min(0),
  total_proteins: zLiver.coerce.number().min(0),
  albumin: zLiver.coerce.number().min(0),
  globulin: zLiver.coerce.number().min(0), // Globulin is required to calculate A/G ratio
});
type LiverFormValues = zLiver.infer<typeof liverSchema>;

interface LiverFormProps {
  patientId: number;
  existingData: LiverAssessment | null | undefined;
  onFormSubmit: () => void;
}

const LiverAssessmentForm: React.FC<LiverFormProps> = ({ patientId, existingData, onFormSubmit }) => {
  const [error, setError] = useStateLiver<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useStateLiver(false);
  
  const { register, handleSubmit, formState: { errors } } = useLiverForm<LiverFormValues>({
    resolver: zodLiverResolver(liverSchema),
    defaultValues: existingData || {},
  });
  
  const onSubmit: LiverSubmitHandler<LiverFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.post(`/patients/${patientId}/assessments/liver`, data);
      toastLiver.success('Liver assessment saved!');
      onFormSubmit();
    } catch (err: any) {
      const msg = err.response?.data?.error || 'Failed to save assessment.';
      setError(msg);
      toastLiver.error('Save failed', { description: msg });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 bg-muted/50 rounded-lg space-y-4">
      {error && (
        <AlertLiver variant="destructive">
          <AlertCircleLiver className="h-4 w-4" />
          <AlertTitleLiver>Error</AlertTitleLiver>
          <AlertDescriptionLiver>{error}</AlertDescriptionLiver>
        </AlertLiver>
      )}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Form Fields */}
        <div className="space-y-2">
          <LabelLiver htmlFor="total_bilirubin">Total Bilirubin</LabelLiver>
          <InputLiver id="total_bilirubin" type="number" step="0.1" {...register('total_bilirubin')} />
          {errors.total_bilirubin && <p className="text-red-500 text-sm">{errors.total_bilirubin.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelLiver htmlFor="direct_bilirubin">Direct Bilirubin</LabelLiver>
          <InputLiver id="direct_bilirubin" type="number" step="0.1" {...register('direct_bilirubin')} />
          {errors.direct_bilirubin && <p className="text-red-500 text-sm">{errors.direct_bilirubin.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelLiver htmlFor="alkaline_phosphotase">Alkaline Phosphotase</LabelLiver>
          <InputLiver id="alkaline_phosphotase" type="number" step="0.1" {...register('alkaline_phosphotase')} />
          {errors.alkaline_phosphotase && <p className="text-red-500 text-sm">{errors.alkaline_phosphotase.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelLiver htmlFor="alamine_aminotransferase">Alamine Aminotransferase</LabelLiver>
          <InputLiver id="alamine_aminotransferase" type="number" step="0.1" {...register('alamine_aminotransferase')} />
          {errors.alamine_aminotransferase && <p className="text-red-500 text-sm">{errors.alamine_aminotransferase.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelLiver htmlFor="aspartate_aminotransferase">Aspartate Aminotransferase</LabelLiver>
          <InputLiver id="aspartate_aminotransferase" type="number" step="0.1" {...register('aspartate_aminotransferase')} />
          {errors.aspartate_aminotransferase && <p className="text-red-500 text-sm">{errors.aspartate_aminotransferase.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelLiver htmlFor="total_proteins">Total Proteins</LabelLiver>
          <InputLiver id="total_proteins" type="number" step="0.1" {...register('total_proteins')} />
          {errors.total_proteins && <p className="text-red-500 text-sm">{errors.total_proteins.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelLiver htmlFor="albumin">Albumin</LabelLiver>
          <InputLiver id="albumin" type="number" step="0.1" {...register('albumin')} />
          {errors.albumin && <p className="text-red-500 text-sm">{errors.albumin.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelLiver htmlFor="globulin">Globulin</LabelLiver>
          <InputLiver id="globulin" type="number" step="0.1" {...register('globulin')} />
          {errors.globulin && <p className="text-red-500 text-sm">{errors.globulin.message}</p>}
        </div>
      </div>
      <ButtonLiver type="submit" disabled={isSubmitting}>
        {isSubmitting && <Loader2Liver className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Liver Assessment
      </ButtonLiver>
    </form>
  );
};
export default LiverAssessmentForm;

// HealthCare App/src/components/admin/forms/HeartAssessmentForm.tsx
import { useForm as useHeartForm, SubmitHandler as HeartSubmitHandler, Controller as HeartController } from 'react-hook-form';
import { zodResolver as zodHeartResolver } from '@hookform/resolvers/zod';
import { z as zHeart } from 'zod';
import { Input as InputHeart } from '@/components/ui/input';
import { Label as LabelHeart } from '@/components/ui/label';
import { Select as SelectHeart, SelectContent as SelectContentHeart, SelectItem as SelectItemHeart, SelectTrigger as SelectTriggerHeart, SelectValue as SelectValueHeart } from '@/components/ui/select';
import { HeartAssessment } from '@/types';
import { useState as useStateHeart } from 'react';
import apiClient from '@/utils/apiClient';
import { toast as toastHeart } from 'sonner';
import { Alert as AlertHeart, AlertDescription as AlertDescriptionHeart, AlertTitle as AlertTitleHeart } from '@/components/ui/alert';
import { Button as ButtonHeart } from '@/components/ui/button';
import { Loader2 as Loader2Heart, AlertCircle as AlertCircleHeart } from 'lucide-react';

// Schema from backend app/schemas.py
const heartSchema = zHeart.object({
  chest_pain_type: zHeart.coerce.number().int().min(0),
  resting_blood_pressure: zHeart.coerce.number().min(0),
  cholesterol: zHeart.coerce.number().min(0),
  fasting_blood_sugar: zHeart.coerce.number().int().min(0).max(1), // 0 or 1
  resting_ecg: zHeart.coerce.number().int().min(0),
  max_heart_rate: zHeart.coerce.number().min(0),
  exercise_angina: zHeart.coerce.number().int().min(0).max(1), // 0 or 1
  st_depression: zHeart.coerce.number().min(0),
  st_slope: zHeart.coerce.number().int().min(0),
});
type HeartFormValues = zHeart.infer<typeof heartSchema>;

interface HeartFormProps {
  patientId: number;
  existingData: HeartAssessment | null | undefined;
  onFormSubmit: () => void;
}

const HeartAssessmentForm: React.FC<HeartFormProps> = ({ patientId, existingData, onFormSubmit }) => {
  const [error, setError] = useStateHeart<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useStateHeart(false);
  
  const { register, handleSubmit, control, formState: { errors } } = useHeartForm<HeartFormValues>({
    resolver: zodHeartResolver(heartSchema),
    defaultValues: existingData ? {
      ...existingData,
      // Ensure select values are strings if that's what <Select> expects
      fasting_blood_sugar: existingData.fasting_blood_sugar,
      exercise_angina: existingData.exercise_angina,
    } : {},
  });
  
  const onSubmit: HeartSubmitHandler<HeartFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.post(`/patients/${patientId}/assessments/heart`, data);
      toastHeart.success('Heart assessment saved!');
      onFormSubmit();
    } catch (err: any) {
      const msg = err.response?.data?.error || 'Failed to save assessment.';
      setError(msg);
      toastHeart.error('Save failed', { description: msg });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 bg-muted/50 rounded-lg space-y-4">
      {error && (
        <AlertHeart variant="destructive">
          <AlertCircleHeart className="h-4 w-4" />
          <AlertTitleHeart>Error</AlertTitleHeart>
          <AlertDescriptionHeart>{error}</AlertDescriptionHeart>
        </AlertHeart>
      )}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {/* Form Fields */}
        <div className="space-y-2">
          <LabelHeart htmlFor="chest_pain_type">Chest Pain Type (0-3)</LabelHeart>
          <InputHeart id="chest_pain_type" type="number" {...register('chest_pain_type')} />
          {errors.chest_pain_type && <p className="text-red-500 text-sm">{errors.chest_pain_type.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="resting_blood_pressure">Resting BP</LabelHeart>
          <InputHeart id="resting_blood_pressure" type="number" step="0.1" {...register('resting_blood_pressure')} />
          {errors.resting_blood_pressure && <p className="text-red-500 text-sm">{errors.resting_blood_pressure.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="cholesterol">Cholesterol</LabelHeart>
          <InputHeart id="cholesterol" type="number" step="0.1" {...register('cholesterol')} />
          {errors.cholesterol && <p className="text-red-500 text-sm">{errors.cholesterol.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="fasting_blood_sugar">Fasting Blood Sugar > 120?</LabelHeart>
          <HeartController
            name="fasting_blood_sugar"
            control={control}
            render={({ field }) => (
              <SelectHeart onValueChange={(val) => field.onChange(parseInt(val))} defaultValue={String(field.value ?? 0)}>
                <SelectTriggerHeart><SelectValueHeart /></SelectTriggerHeart>
                <SelectContentHeart>
                  <SelectItemHeart value="0">No (<= 120 mg/dl)</SelectItemHeart>
                  <SelectItemHeart value="1">Yes (> 120 mg/dl)</SelectItemHeart>
                </SelectContentHeart>
              </SelectHeart>
            )}
          />
          {errors.fasting_blood_sugar && <p className="text-red-500 text-sm">{errors.fasting_blood_sugar.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="resting_ecg">Resting ECG (0-2)</LabelHeart>
          <InputHeart id="resting_ecg" type="number" {...register('resting_ecg')} />
          {errors.resting_ecg && <p className="text-red-500 text-sm">{errors.resting_ecg.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="max_heart_rate">Max Heart Rate</LabelHeart>
          <InputHeart id="max_heart_rate" type="number" step="0.1" {...register('max_heart_rate')} />
          {errors.max_heart_rate && <p className="text-red-500 text-sm">{errors.max_heart_rate.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="exercise_angina">Exercise-induced Angina?</LabelHeart>
          <HeartController
            name="exercise_angina"
            control={control}
            render={({ field }) => (
              <SelectHeart onValueChange={(val) => field.onChange(parseInt(val))} defaultValue={String(field.value ?? 0)}>
                <SelectTriggerHeart><SelectValueHeart /></SelectTriggerHeart>
                <SelectContentHeart>
                  <SelectItemHeart value="0">No</SelectItemHeart>
                  <SelectItemHeart value="1">Yes</SelectItemHeart>
                </SelectContentHeart>
              </SelectHeart>
            )}
          />
          {errors.exercise_angina && <p className="text-red-500 text-sm">{errors.exercise_angina.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="st_depression">ST Depression</LabelHeart>
          <InputHeart id="st_depression" type="number" step="0.1" {...register('st_depression')} />
          {errors.st_depression && <p className="text-red-500 text-sm">{errors.st_depression.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelHeart htmlFor="st_slope">ST Slope (0-2)</LabelHeart>
          <InputHeart id="st_slope" type="number" {...register('st_slope')} />
          {errors.st_slope && <p className="text-red-500 text-sm">{errors.st_slope.message}</p>}
        </div>
      </div>
      <ButtonHeart type="submit" disabled={isSubmitting}>
        {isSubmitting && <Loader2Heart className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Heart Assessment
      </ButtonHeart>
    </form>
  );
};
export default HeartAssessmentForm;

// HealthCare App/src/components/admin/forms/MentalHealthAssessmentForm.tsx
import { useForm as useMentalForm, SubmitHandler as MentalSubmitHandler, Controller as MentalController } from 'react-hook-form';
import { zodResolver as zodMentalResolver } from '@hookform/resolvers/zod';
import { z as zMental } from 'zod';
import { Input as InputMental } from '@/components/ui/input';
import { Label as LabelMental } from '@/components/ui/label';
import { Textarea as TextareaMental } from '@/components/ui/textarea';
import { Select as SelectMental, SelectContent as SelectContentMental, SelectItem as SelectItemMental, SelectTrigger as SelectTriggerMental, SelectValue as SelectValueMental } from '@/components/ui/select';
import { MentalHealthAssessment } from '@/types';
import { useState as useStateMental } from 'react';
import apiClient from '@/utils/apiClient';
import { toast as toastMental } from 'sonner';
import { Alert as AlertMental, AlertDescription as AlertDescriptionMental, AlertTitle as AlertTitleMental } from '@/components/ui/alert';
import { Button as ButtonMental } from '@/components/ui/button';
import { Loader2 as Loader2Mental, AlertCircle as AlertCircleMental } from 'lucide-react';

// Schema from backend app/schemas.py
const mentalHealthSchema = zMental.object({
  phq_score: zMental.coerce.number().int().min(0).max(27),
  gad_score: zMental.coerce.number().int().min(0).max(21),
  sleep_quality: zMental.coerce.number().int().min(1).max(5),
  mood_factors: zMental.string().max(255).optional().nullable(),
});
type MentalFormValues = zMental.infer<typeof mentalHealthSchema>;

interface MentalFormProps {
  patientId: number;
  existingData: MentalHealthAssessment | null | undefined;
  onFormSubmit: () => void;
}

const MentalHealthAssessmentForm: React.FC<MentalFormProps> = ({ patientId, existingData, onFormSubmit }) => {
  const [error, setError] = useStateMental<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useStateMental(false);
  
  const { register, handleSubmit, control, formState: { errors } } = useMentalForm<MentalFormValues>({
    resolver: zodMentalResolver(mentalHealthSchema),
    defaultValues: existingData || {},
  });
  
  const onSubmit: MentalSubmitHandler<MentalFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.post(`/patients/${patientId}/assessments/mental_health`, data);
      toastMental.success('Mental Health assessment saved!');
      onFormSubmit();
    } catch (err: any) {
      const msg = err.response?.data?.error || 'Failed to save assessment.';
      setError(msg);
      toastMental.error('Save failed', { description: msg });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 bg-muted/50 rounded-lg space-y-4">
      {error && (
        <AlertMental variant="destructive">
          <AlertCircleMental className="h-4 w-4" />
          <AlertTitleMental>Error</AlertTitleMental>
          <AlertDescriptionMental>{error}</AlertDescriptionMental>
        </AlertMental>
      )}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Form Fields */}
        <div className="space-y-2">
          <LabelMental htmlFor="phq_score">PHQ-9 Score (0-27)</LabelMental>
          <InputMental id="phq_score" type="number" {...register('phq_score')} />
          {errors.phq_score && <p className="text-red-500 text-sm">{errors.phq_score.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelMental htmlFor="gad_score">GAD-7 Score (0-21)</LabelMental>
          <InputMental id="gad_score" type="number" {...register('gad_score')} />
          {errors.gad_score && <p className="text-red-500 text-sm">{errors.gad_score.message}</p>}
        </div>
        <div className="space-y-2">
          <LabelMental htmlFor="sleep_quality">Sleep Quality (1-5)</LabelMental>
           <MentalController
            name="sleep_quality"
            control={control}
            render={({ field }) => (
              <SelectMental onValueChange={(val) => field.onChange(parseInt(val))} defaultValue={String(field.value ?? 3)}>
                <SelectTriggerMental><SelectValueMental placeholder="Select quality" /></SelectTriggerMental>
                <SelectContentMental>
                  <SelectItemMental value="1">1 (Very Poor)</SelectItemMental>
                  <SelectItemMental value="2">2 (Poor)</SelectItemMental>
                  <SelectItemMental value="3">3 (Average)</SelectItemMental>
                  <SelectItemMental value="4">4 (Good)</SelectItemMental>
                  <SelectItemMental value="5">5 (Very Good)</SelectItemMental>
                </SelectContentMental>
              </SelectMental>
            )}
          />
          {errors.sleep_quality && <p className="text-red-500 text-sm">{errors.sleep_quality.message}</p>}
        </div>
      </div>
      <div className="space-y-2">
        <LabelMental htmlFor="mood_factors">Mood Factors (Optional)</LabelMental>
        <TextareaMental id="mood_factors" {...register('mood_factors')} placeholder="e.g., Stress at work, family issues..." />
        {errors.mood_factors && <p className="text-red-500 text-sm">{errors.mood_factors.message}</p>}
      </div>
      <ButtonMental type="submit" disabled={isSubmitting}>
        {isSubmitting && <Loader2Mental className="mr-2 h-4 w-4 animate-spin" />}
        {existingData ? 'Update' : 'Save'} Mental Health Assessment
      </ButtonMental>
    </form>
  );
};
export default MentalHealthAssessmentForm;