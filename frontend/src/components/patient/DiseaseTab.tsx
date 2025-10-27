// HealthCare App/src/components/patient/DiseaseTab.tsx
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/components/ui/utils';
import { LifestyleRecommendation } from '@/types';
import RecommendationCard from './RecommendationCard';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

interface DiseaseTabProps {
  title: string;
  riskLevel: 'Low' | 'Medium' | 'High' | null | undefined;
  riskScore: number | null | undefined;
  recommendations: LifestyleRecommendation[];
  assessmentData: any | null | undefined; // The raw assessment data
}

const DiseaseTab: React.FC<DiseaseTabProps> = ({
  title,
  riskLevel,
  riskScore,
  recommendations,
  assessmentData,
}) => {
  const getRiskBadgeClassName = (level: string | null | undefined): string => {
    switch (level) {
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low': return 'bg-green-100 text-green-800 border-green-200';
      default: return '';
    }
  };

  const riskCategories = {
    Diet: recommendations.filter(r => r.category === 'Diet'),
    Exercise: recommendations.filter(r => r.category === 'Exercise'),
    Sleep: recommendations.filter(r => r.category === 'Sleep'),
    Lifestyle: recommendations.filter(r => r.category === 'Lifestyle'),
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{title} Dashboard</CardTitle>
          {!assessmentData ? (
             <CardDescription className="flex items-center gap-2 text-yellow-600">
               <AlertCircle className="h-4 w-4" />
               Your risk profile is pending. Please have an admin complete your assessment.
             </CardDescription>
          ) : (
             <CardDescription className="flex items-center gap-2 text-green-600">
               <CheckCircle2 className="h-4 w-4" />
               Your profile is up to date. Last assessed on {new Date(assessmentData.assessed_at).toLocaleDateString()}.
             </CardDescription>
          )}
        </CardHeader>
        <CardContent className="flex items-center gap-4">
          <div className="text-center p-6 bg-muted/50 rounded-lg">
            <div className="text-sm text-muted-foreground">Your Risk Level</div>
            <Badge
              className={cn(
                getRiskBadgeClassName(riskLevel),
                'text-2xl font-bold px-6 py-2 mt-2'
              )}
            >
              {riskLevel || 'N/A'}
            </Badge>
          </div>
          <div className="text-center p-6 bg-muted/50 rounded-lg flex-1">
            <div className="text-sm text-muted-foreground">Prediction Score</div>
            <div className="text-4xl font-bold">
              {riskScore ? `${(riskScore * 100).toFixed(1)}%` : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              {riskScore ? `(A ${riskScore * 100 > 50 ? 'higher' : 'lower'} score indicates risk)` : 'No score generated.'}
            </p>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Personalized Lifestyle Guidance</CardTitle>
          <CardDescription>
            Recommendations for diet, exercise, and habits based on your {title} risk.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {recommendations.length === 0 && (
            <p className="text-muted-foreground">
              No specific recommendations available for your current risk level.
            </p>
          )}
          
          {riskCategories.Diet.length > 0 && (
            <RecommendationCard 
              title="Diet"
              recommendation={riskCategories.Diet[0]} 
            />
          )}
          {riskCategories.Exercise.length > 0 && (
            <RecommendationCard 
              title="Exercise"
              recommendation={riskCategories.Exercise[0]} 
            />
          )}
          {riskCategories.Sleep.length > 0 && (
            <RecommendationCard 
              title="Sleep"
              recommendation={riskCategories.Sleep[0]} 
            />
          )}
          {riskCategories.Lifestyle.length > 0 && (
            <RecommendationCard 
              title="Lifestyle"
              recommendation={riskCategories.Lifestyle[0]} 
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default DiseaseTab;