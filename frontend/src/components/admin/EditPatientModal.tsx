// HealthCare App/frontend/src/components/admin/EditPatientModal.tsx
import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle, Loader2 } from 'lucide-react';
import { useForm, Controller, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import apiClient from '@/utils/apiClient';
import { PatientUser } from '@/types';
import { toast } from 'sonner';

// Zod schema for Patient Update (Subset of fields)
const patientUpdateSchema = z.object({
  full_name: z.string().min(2, 'Full name must be at least 2 characters'),
  age: z.coerce.number().int().gt(0, 'Age must be a positive number'),
  gender: z.enum(['Male', 'Female', 'Other']),
  height_cm: z.coerce.number().gt(0, 'Height must be positive'),
  weight_kg: z.coerce.number().gt(0, 'Weight must be positive'),
  state_name: z.string().min(2, 'State name is required'),
});

type PatientUpdateFormValues = z.infer<typeof patientUpdateSchema>;

interface EditPatientModalProps {
  isOpen: boolean;
  onClose: () => void;
  patient: PatientUser | null;
  onPatientUpdated: () => void;
}

const EditPatientModal: React.FC<EditPatientModalProps> = ({
  isOpen,
  onClose,
  patient,
  onPatientUpdated,
}) => {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<PatientUpdateFormValues>({
    resolver: zodResolver(patientUpdateSchema),
  });

  // Reset form when patient data changes or modal opens/closes
  useEffect(() => {
    if (patient) {
      reset({
        full_name: patient.full_name,
        age: patient.age,
        gender: patient.gender as 'Male' | 'Female' | 'Other',
        height_cm: patient.height_cm,
        weight_kg: patient.weight_kg,
        state_name: patient.state_name || '',
      });
    } else {
        reset(); // Clear if no patient
    }
    setError(null); // Clear errors on open/close
  }, [patient, isOpen, reset]);


  // Handle Form Submission
  const onSubmit: SubmitHandler<PatientUpdateFormValues> = async (data) => {
    if (!patient) return;

    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.put(`/patients/${patient.id}`, data);
      toast.success("Patient details updated successfully.");
      onPatientUpdated(); // Notify parent to refresh and close modal
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'Failed to update patient.';
      setError(errorMsg);
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-lg">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Patient Details</DialogTitle>
            <DialogDescription>
              Update the patient's demographic information. ABHA ID cannot be changed.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Update Failed</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Form Fields */}
            <div className="space-y-2">
              <Label htmlFor="edit_full_name">Full Name</Label>
              <Input id="edit_full_name" {...register('full_name')} />
              {errors.full_name && <p className="text-destructive text-sm">{errors.full_name.message}</p>}
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="edit_age">Age</Label>
                <Input id="edit_age" type="number" {...register('age')} />
                {errors.age && <p className="text-destructive text-sm">{errors.age.message}</p>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit_gender">Gender</Label>
                <Controller
                  name="gender"
                  control={control}
                  render={({ field }) => (
                    <Select onValueChange={field.onChange} value={field.value}>
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Male">Male</SelectItem>
                        <SelectItem value="Female">Female</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                />
                {errors.gender && <p className="text-destructive text-sm">{errors.gender.message}</p>}
              </div>
               <div className="space-y-2">
                <Label htmlFor="edit_state_name">State</Label>
                <Input id="edit_state_name" {...register('state_name')} />
                {errors.state_name && <p className="text-destructive text-sm">{errors.state_name.message}</p>}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
               <div className="space-y-2">
                <Label htmlFor="edit_height_cm">Height (cm)</Label>
                <Input id="edit_height_cm" type="number" step="0.1" {...register('height_cm')} />
                {errors.height_cm && <p className="text-destructive text-sm">{errors.height_cm.message}</p>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit_weight_kg">Weight (kg)</Label>
                <Input id="edit_weight_kg" type="number" step="0.1" {...register('weight_kg')} />
                {errors.weight_kg && <p className="text-destructive text-sm">{errors.weight_kg.message}</p>}
              </div>
            </div>

          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              Save Changes
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default EditPatientModal;