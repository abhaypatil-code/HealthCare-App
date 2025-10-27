// HealthCare App/src/components/admin/ConsultationModal.tsx
import React, { useState } from 'react';
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
import { Textarea } from '@/components/ui/textarea';
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

// Zod schema for Consultation Booking
const consultationSchema = z.object({
  consultation_type: z.enum(['Teleconsultation', 'In-Person']),
  // Use string for datetime-local input, then convert
  consultation_datetime_str: z.string().min(1, "Please select a date and time"),
  notes: z.string().optional().nullable(),
});

type ConsultationFormValues = z.infer<typeof consultationSchema>;

interface ConsultationModalProps {
  isOpen: boolean;
  onClose: () => void;
  patientId: number;
  onConsultationBooked: () => void;
}

const ConsultationModal: React.FC<ConsultationModalProps> = ({
  isOpen,
  onClose,
  patientId,
  onConsultationBooked,
}) => {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<ConsultationFormValues>({
    resolver: zodResolver(consultationSchema),
    defaultValues: {
      consultation_type: 'Teleconsultation',
    },
  });

  // Handle Modal Close
  const handleClose = () => {
    reset(); // Reset form
    setError(null);
    onClose();
  };

  // Handle Form Submission
  const onSubmit: SubmitHandler<ConsultationFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      // Convert local datetime string to ISO string for the backend
      const isoDateTime = new Date(data.consultation_datetime_str).toISOString();
      
      const payload = {
        patient_id: patientId,
        consultation_type: data.consultation_type,
        consultation_datetime_str: isoDateTime, // Send as ISO string
        notes: data.notes,
      };

      await apiClient.post('/consultations', payload);
      
      onConsultationBooked(); // Notify parent to refresh and close
      
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'Failed to book consultation.';
      setError(errorMsg);
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Book Consultation</DialogTitle>
            <DialogDescription>
              Schedule a new (dummy) consultation for this patient.
            </DialogDescription>
          </DialogHeader>
          
          <div className="grid gap-4 py-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Booking Failed</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="consultation_type">Type</Label>
              <Controller
                name="consultation_type"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select consultation type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Teleconsultation">Teleconsultation (Medium Risk)</SelectItem>
                      <SelectItem value="In-Person">In-Person (High Risk)</SelectItem>
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.consultation_type && (
                <p className="text-red-500 text-sm">{errors.consultation_type.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="consultation_datetime_str">Date & Time</Label>
              <Input
                id="consultation_datetime_str"
                type="datetime-local"
                {...register('consultation_datetime_str')}
              />
              {errors.consultation_datetime_str && (
                <p className="text-red-500 text-sm">{errors.consultation_datetime_str.message}</p>
              )}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="notes">Notes (Optional)</Label>
              <Textarea
                id="notes"
                placeholder="e.g., Follow-up for high heart risk"
                {...register('notes')}
              />
              {errors.notes && (
                <p className="text-red-500 text-sm">{errors.notes.message}</p>
              )}
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={handleClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : null}
              Book Consultation
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default ConsultationModal;