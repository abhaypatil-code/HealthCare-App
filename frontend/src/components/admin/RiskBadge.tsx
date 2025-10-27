// HealthCare App/src/components/admin/RiskBadge.tsx
import React from 'react';
import { Badge } from '@/components/ui/badge';
import { RiskPrediction } from '@/types';
import { cn } from '@/components/ui/utils'; // Make sure you have this utility

interface RiskBadgeProps {
  prediction: RiskPrediction | null | undefined;
  condensed?: boolean;
}

/**
 * A component to display a patient's highest risk level as a color-coded badge.
 */
const RiskBadge: React.FC<RiskBadgeProps> = ({ prediction, condensed = false }) => {
  if (!prediction) {
    return <Badge variant="outline">N/A</Badge>;
  }

  const levels = [
    prediction.diabetes_level,
    prediction.heart_level,
    prediction.liver_level,
    prediction.mental_health_level,
  ];

  let highestRisk = 'Low';
  if (levels.includes('High')) {
    highestRisk = 'High';
  } else if (levels.includes('Medium')) {
    highestRisk = 'Medium';
  } else if (!levels.some(level => level === null || level === undefined)) {
    // Only show 'Low' if all predictions are present and are 'Low'
    highestRisk = 'Low';
  } else {
    // If some predictions are missing but none are Med/High
    return <Badge variant="outline">Pending</Badge>;
  }

  const variant = {
    Low: 'default', // Green (default badge is black, we'll override)
    Medium: 'secondary', // Yellow
    High: 'destructive', // Red
  }[highestRisk];

  const className = cn(
    {
      'bg-green-100 text-green-800 border-green-200': highestRisk === 'Low',
      'bg-yellow-100 text-yellow-800 border-yellow-200': highestRisk === 'Medium',
      'bg-red-100 text-red-800 border-red-200': highestRisk === 'High',
    },
    'border' // Add border for all
  );

  if (condensed) {
    return (
      <Badge variant={variant as any} className={className}>
        {highestRisk}
      </Badge>
    );
  }

  // A more detailed view (not used in the table)
  return (
    <div className="flex flex-col gap-2">
      <Badge variant={variant as any} className={cn(className, 'text-lg px-4 py-1')}>
        Overall Risk: {highestRisk}
      </Badge>
      <div className="grid grid-cols-2 gap-1 text-sm">
        <Badge variant={prediction.diabetes_level === 'High' ? 'destructive' : 'outline'}>
          Diabetes: {prediction.diabetes_level || 'N/A'}
        </Badge>
         <Badge variant={prediction.heart_level === 'High' ? 'destructive' : 'outline'}>
          Heart: {prediction.heart_level || 'N/A'}
        </Badge>
         <Badge variant={prediction.liver_level === 'High' ? 'destructive' : 'outline'}>
          Liver: {prediction.liver_level || 'N/A'}
        </Badge>
         <Badge variant={prediction.mental_health_level === 'High' ? 'destructive' : 'outline'}>
          Mental Health: {prediction.mental_health_level || 'N/A'}
        </Badge>
      </div>
    </div>
  );
};

export default RiskBadge;