// HealthCare App/frontend/src/hooks/usePdfDownload.ts
import { useState } from 'react';
import { saveAs } from 'file-saver';
import apiClient from '@/utils/apiClient';
import { toast } from 'sonner';

interface PdfOptions {
  include_demographics?: boolean;
  include_risk_summary?: boolean;
  include_recommendations?: boolean;
}

const usePdfDownload = () => {
  const [isDownloading, setIsDownloading] = useState(false);

  const downloadPdf = async (patientId: number | string, abhaId: string | undefined, options: PdfOptions = {}) => {
    setIsDownloading(true);
    const toastId = toast.info("Generating PDF report...");

    const reportOptions = {
      include_demographics: options.include_demographics ?? true,
      include_risk_summary: options.include_risk_summary ?? true,
      include_recommendations: options.include_recommendations ?? true,
    };

    try {
      const response = await apiClient.post(
        `/reports/patient/${patientId}/download`,
        reportOptions,
        { responseType: 'blob' }
      );

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const filename = `Patient_Report_${abhaId || patientId}.pdf`;
      saveAs(blob, filename);

      toast.success("Report downloaded", { id: toastId });
    } catch (err) {
      console.error("PDF Download Error:", err);
      toast.error("Failed to generate report", {
        id: toastId,
        description: (err as any).response?.data?.message || 'An unexpected error occurred.',
      });
    } finally {
      setIsDownloading(false);
    }
  };

  return { isDownloading, downloadPdf };
};

export default usePdfDownload;