declare function useHostServiceQuery(): <TResponse, TRequest = Record<string, unknown>>(
  serviceId: number,
  query?: TRequest,
  pathParams?: Record<string, string>,
  options?: Record<string, unknown>,
) => TResponse | undefined;

declare function useHostServiceMutation(): <TResponse, TRequest>(serviceId: number) => {
  mutate: (data: TRequest, options?: { onSuccess?: () => void }) => TResponse | undefined;
  isPending: boolean;
};

declare function useHostServiceBlobMutation(): <TRequest>(serviceId: number) => {
  mutate: (
    data: TRequest & { pathParams: Record<string, string> },
    options?: { onSuccess?: (blob: Blob) => void },
  ) => void;
  isPending: boolean;
};

const FeatureService = {
  GetEntities: 100,
  GetEntityById: 101,
  PostCreateEntity: 102,
  PutUpdateEntity: 103,
  DeleteEntity: 104,
  PostVerbEntity: 110,
  PostRemoveSubEntity: 202,
  PostGenerateEntityBlob: 300,
} as const;

interface SubEntityItem {
  subEntityId: number;
  order: number;
}

interface EntityListItem {
  entityId: number;
  code: string;
  name: string;
  status: StatusItem;
}

interface EntityDetail extends EntityListItem {
  subEntities: SubEntityItem[];
  summary: {
    totalSubEntities: number;
    totalAmount: number;
  };
}

interface StatusItem {
  masterTableId: number;
  name: string;
  value: string;
  backgroundColor?: string | null;
  textColor?: string | null;
}

interface EntitiesQueryParams extends Record<string, unknown> {
  page?: number;
  pageSize?: number;
  search?: string | null;
  statusId?: number | null;
  sortBy?: string | null;
  sortOrder?: string | null;
}

interface EntitiesResponse {
  success: boolean;
  data: { items: EntityListItem[] };
  pagination: { page: number; pageSize: number; totalRecords: number; totalPages: number };
  message: string;
}

export function useEntities(params?: EntitiesQueryParams, enabled = true) {
  const createQuery = useHostServiceQuery();
  return createQuery<EntitiesResponse, EntitiesQueryParams>(
    FeatureService.GetEntities,
    params,
    undefined,
    { enabled, staleTime: 0 }
  );
}

interface EntityResponse {
  success: boolean;
  data: { item: EntityDetail };
  message: string;
}

export function useEntity(id: number, enabled = true) {
  const createQuery = useHostServiceQuery();
  return createQuery<EntityResponse>(
    FeatureService.GetEntityById,
    undefined,
    { id: id.toString() },
    { enabled }
  );
}

interface CreateEntityRequest extends Record<string, unknown> {
  name: string;
  fieldId: number;
}

interface CreateEntityResponse {
  success: boolean;
  data: { item: { entityId: number; code: string; name: string } };
  message: string;
}

export function useCreateEntity() {
  const createServiceMutation = useHostServiceMutation();
  const createMutation = createServiceMutation<CreateEntityResponse, CreateEntityRequest>(
    FeatureService.PostCreateEntity,
  );

  return {
    create: (data: CreateEntityRequest, options?: { onSuccess?: () => void }) =>
      createMutation.mutate(data, {
        onSuccess: () => options?.onSuccess?.(),
      }),
    isPending: createMutation.isPending,
  };
}

interface UpdateEntityRequest extends Record<string, unknown> {
  name?: string;
  fieldId?: number;
}

interface UpdateEntityResponse {
  success: boolean;
  data: { item: { entityId: number; name: string } };
  message: string;
}

export function useUpdateEntity() {
  const createServiceMutation = useHostServiceMutation();
  const updateMutation = createServiceMutation<UpdateEntityResponse, UpdateEntityRequest>(
    FeatureService.PutUpdateEntity,
  );

  return {
    update: (data: UpdateEntityRequest, options?: { onSuccess?: () => void }) =>
      updateMutation.mutate(data, {
        onSuccess: () => options?.onSuccess?.(),
      }),
    isPending: updateMutation.isPending,
  };
}

interface DeleteEntityResponse {
  success: boolean;
  data: { result: string; deletedEntityId: number; message: string };
  message: string;
}

export function useDeleteEntity() {
  const createServiceMutation = useHostServiceMutation();
  const deleteMutation = createServiceMutation<DeleteEntityResponse, Record<string, unknown>>(
    FeatureService.DeleteEntity,
  );

  return {
    remove: (options?: { onSuccess?: () => void }) =>
      deleteMutation.mutate({}, {
        onSuccess: () => options?.onSuccess?.(),
      }),
    isPending: deleteMutation.isPending,
  };
}

interface VerbEntityRequest extends Record<string, unknown> {
  optionalField?: string | null;
}

interface VerbEntityResponse {
  success: boolean;
  data: {
    item: {
      entityId: number;
      code: string;
      status: StatusItem;
    };
  };
  message: string;
}

export function useVerbEntity() {
  const createServiceMutation = useHostServiceMutation();
  const verbMutation = createServiceMutation<VerbEntityResponse, VerbEntityRequest>(
    FeatureService.PostVerbEntity,
  );

  return {
    verb: (data: VerbEntityRequest, options?: { onSuccess?: () => void }) =>
      verbMutation.mutate(data, {
        onSuccess: () => options?.onSuccess?.(),
      }),
    isPending: verbMutation.isPending,
  };
}

interface RemoveSubEntityRequest extends Record<string, unknown> {
  justification: string;
}

interface RemoveSubEntityResponse {
  success: boolean;
  data: { result: string; removedSubEntityId: number; remainingCount: number; message: string };
  message: string;
}

export function useRemoveSubEntity() {
  const createServiceMutation = useHostServiceMutation();
  const removeMutation = createServiceMutation<RemoveSubEntityResponse, RemoveSubEntityRequest>(
    FeatureService.PostRemoveSubEntity,
  );

  return {
    remove: (data: RemoveSubEntityRequest, options?: { onSuccess?: () => void }) =>
      removeMutation.mutate(data, {
        onSuccess: () => options?.onSuccess?.(),
      }),
    isPending: removeMutation.isPending,
  };
}

export function useGenerateEntityBlob() {
  const createMutation = useHostServiceBlobMutation();
  const mutation = createMutation<Record<string, unknown>>(FeatureService.PostGenerateEntityBlob);

  return {
    generate: (id: number, options?: { onSuccess?: () => void }) =>
      mutation.mutate(
        { pathParams: { id: id.toString() } },
        {
          onSuccess: (blob) => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'Document.pdf';
            link.click();
            window.URL.revokeObjectURL(url);
            options?.onSuccess?.();
          },
        },
      ),
    isPending: mutation.isPending,
  };
}
