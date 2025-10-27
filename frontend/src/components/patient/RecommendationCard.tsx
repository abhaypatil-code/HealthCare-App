// HealthCare App/src/components/patient/RecommendationCard.tsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LifestyleRecommendation } from '@/types';
import { Utensils, Dumbbell, Bed, Smile } from 'lucide-react';

interface RecommendationCardProps {
  title?: string; // Optional title override
  recommendation: LifestyleRecommendation;
}

const iconMap = {
  Diet: <Utensils className="h-5 w-5" />,
  Exercise: <Dumbbell className="h-5 w-5" />,
  Sleep: <Bed className="h-5 w-5" />,
  Lifestyle: <Smile className="h-5 w-5" />,
  general: <Smile className="h-5 w-5" />,
};

const RecommendationCard: React.FC<RecommendationCardProps> = ({ title, recommendation }) => {
  const cardTitle = title || recommendation.category;
  const icon = iconMap[recommendation.category || 'general'];

  return (
    <Card className="bg-white">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-base font-medium capitalize">
          {cardTitle}
        </CardTitle>
        <span className="text-muted-foreground">{icon}</span>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">
          {recommendation.recommendation_text}
        </p>
      </CardContent>
    </Card>
  );
};

export default RecommendationCard;