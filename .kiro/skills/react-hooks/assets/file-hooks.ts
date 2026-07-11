// hooks/useFileUpload.ts - S3 Presigned URL Upload

interface UploadFileParams {
  file: File;
  prefix?: string;
  onProgress?: (progress: number) => void;
}

interface UploadFileResult {
  filePath: string;
  fileName: string;
  fileSize: number;
  contentType: string;
}

export const useFileUpload = (serviceId: number) => {
  const { getServiceById } = useCurrentOption();
  const service = getServiceById(serviceId);

  return useMutation<UploadFileResult, Error, UploadFileParams>({
    mutationFn: async ({ file, prefix, onProgress }) => {
      if (!service) throw new Error(`No access to service: ${serviceId}`);

      // 1. Get presigned URL
      const { uploadUrl, filePath } = await apiClient<{
        uploadUrl: string;
        filePath: string;
      }>(service.Path, {
        method: service.Method,
        json: {
          fileName: file.name,
          contentType: file.type,
          fileSizeKB: Math.ceil(file.size / 1024),
          prefix,
        },
      });

      // 2. Upload to S3
      await ky.put(uploadUrl, {
        body: file,
        headers: { 'Content-Type': file.type },
        onUploadProgress: onProgress
          ? (p) => onProgress(Math.round((p.transferredBytes / p.totalBytes) * 100))
          : undefined,
      });

      return {
        filePath,
        fileName: file.name,
        fileSize: Math.ceil(file.size / 1024),
        contentType: file.type,
      };
    },
  });
};

// ---------------------------------------------------------------------------
// hooks/useDownloadFile.ts - S3 Presigned URL Download

interface DownloadParams {
  filePath: string;
  fileName?: string;
}

export const useDownloadFile = (serviceId: number) => {
  const { getServiceById } = useCurrentOption();
  const service = getServiceById(serviceId);

  return useMutation<{ downloadUrl: string | null }, Error, DownloadParams>({
    mutationFn: async ({ filePath, fileName }) => {
      if (!service) throw new Error(`No access to service: ${serviceId}`);

      const params = new URLSearchParams({ filePath });
      if (fileName) params.append('fileName', fileName);

      return apiClient(`${service.Path}?${params}`, { method: service.Method });
    },
    onSuccess: (data) => {
      if (data.downloadUrl) window.open(data.downloadUrl, '_blank');
    },
  });
};
