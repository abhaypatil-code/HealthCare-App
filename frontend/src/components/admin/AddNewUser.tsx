// HealthCare App/src/components/admin/AddNewUser.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
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
import { toast } from 'sonner';

// --- FIX: Add Strong Password Validation ---
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,}$/;
const PASSWORD_ERROR = "Must be 8+ chars with uppercase, lowercase, number, and special character.";

// Zod schema for Patient Creation (fulfills MVP requirements)
const patientCreateSchema = z.object({
  full_name: z.string().min(2, 'Full name must be at least 2 characters'),
  age: z.coerce.number().int().gt(0, 'Age must be a positive number'),
  gender: z.enum(['Male', 'Female', 'Other']),
  height_cm: z.coerce.number().gt(0, 'Height must be positive'),
  weight_kg: z.coerce.number().gt(0, 'Weight must be positive'),
  abha_id: z.string().regex(/^\d{14}$/, 'ABHA ID must be 14 digits'),
  state_name: z.string().min(2, 'State name is required'),
  password: z.string().regex(PASSWORD_REGEX, PASSWORD_ERROR), // <-- APPLIED FIX
});

type PatientCreateFormValues = z.infer<typeof patientCreateSchema>;

const AddNewUser: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<PatientCreateFormValues>({
    resolver: zodResolver(patientCreateSchema),
    defaultValues: {
      gender: 'Male', // Set a default
    },
  });

  // Handle Patient Creation
  const onSubmit: SubmitHandler<PatientCreateFormValues> = async (data) => {
    setError(null);
    setIsSubmitting(true);
    try {
      const { data: responseData } = await apiClient.post('/patients', data);
      
      toast.success('Patient created successfully', {
        description: `Patient ${responseData.patient.full_name} has been registered.`,
      });
      
      // Redirect to the new patient's detail page to complete assessments
      navigate(`/admin/patients/${responseData.patient.id}`);
      
    } catch (err: any) {
      // --- FIX: Handle Pydantic validation error display ---
      if (err.response?.data?.messages) {
        // Handle Pydantic validation errors
        const pydanticErrors = err.response.data.messages;
        const errorMessages = pydanticErrors.map((e: any) => {
             if (e.loc && e.loc[0] === 'password') return PASSWORD_ERROR;
             return `${e.loc.join('.')}: ${e.msg}`
        }).join(' ');
        setError(errorMessages);
      } else {
        const errorMsg = err.response?.data?.message || 'Failed to create patient.';
        setError(errorMsg);
      }
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <form onSubmit={handleSubmit(onSubmit)}>
        <Card>
          <CardHeader>
            <CardTitle>Register New Patient (Step 1)</CardTitle>
            <CardDescription>
              Enter the patient's basic demographic and login information.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Registration Failed</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Form Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="full_name">Full Name</Label>
                <Input id="full_name" {...register('full_name')} />
                {errors.full_name && (
                  <p className="text-red-500 text-sm">{errors.full_name.message}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="abha_id">ABHA ID (14-digit)</Label>
                <Input id="abha_id" {...register('abha_id')} />
                {errors.abha_id && (
                  <p className="text-red-500 text-sm">{errors.abha_id.message}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="age">Age</Label>
                <Input id="age" type="number" {...register('age')} />
                {errors.age && (
                  <p className="text-red-500 text-sm">{errors.age.message}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="gender">Gender</Label>
                <Controller
                  name="gender"
                  control={control}
                  render={({ field }) => (
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select gender" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Male">Male</SelectItem>
                        <SelectItem value="Female">Female</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                />
                {errors.gender && (
                  <p className="text-red-500 text-sm">{errors.gender.message}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="state_name">State</Label>
                <Input id="state_name" {...register('state_name')} />
                {errors.state_name && (
                  <p className="text-red-500 text-sm">{errors.state_name.message}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="height_cm">Height (cm)</Label>
                <Input id="height_cm" type="number" step="0.1" {...register('height_cm')} />
                {errors.height_cm && (
                  <p className="text-red-500 text-sm">{errors.height_cm.message}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="weight_kg">Weight (kg)</Label>
                <Input id="weight_kg" type="number" step="0.1" {...register('weight_kg')} />
                {errors.weight_kg && (
                  <p className="text-red-500 text-sm">{errors.weight_kg.message}</p>
                )}
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">Initial Password</Label>
              <Input id="password" type="password" {...register('password')} />
              <p className="text-xs text-muted-foreground">
                Set an initial password for the patient to log in.
              </p>
              {errors.password && (
                <p className="text-red-500 text-sm">{errors.password.message}</p>
              )}
            </div>

            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : null}
              Create Patient
            </Button>
          </CardContent>
        </Card>
      </form>
    </div>
  );
};

export default AddNewUser;