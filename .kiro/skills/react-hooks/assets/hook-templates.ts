// Query Hook Template (GET requests)
import { useHostServiceQuery } from '@/shared/adapters';

export interface UsersQueryParams extends QueryParams {
  page: number;
  pageSize: number;
  search?: string;
  statusId?: number;
}

export interface UsersData {
  items: UserListItem[] | null;
}

export interface UsersResponse {
  success: boolean;
  data: UsersData;
  message: string | null;
  pagination: { page: number; pageSize: number; totalRecords: number; /* ... */ };
}

export function useUsers(params?: UsersQueryParams, enabled = true) {
  const createQuery = useHostServiceQuery();
  return createQuery<UsersResponse, UsersQueryParams>(
    UserService.GetUsers,
    params,
    undefined,
    { enabled, staleTime: 0 }
  );
}

// ---------------------------------------------------------------------------
// Mutation Hook Template (POST/PUT/DELETE)
import { useHostServiceMutation } from '@/shared/adapters';

export interface AddUserRequest extends Record<string, unknown> {
  pathParams?: {
    departmentId: string;
  };
  name: string;
  email: string;
}

export function useAddUser() {
  const createServiceMutation = useHostServiceMutation();
  const addMutation = createServiceMutation<AddUserResponse, AddUserRequest>(
    UserService.AddUser,
  );

  return {
    add: (
      departmentId: number,
      data: Omit<AddUserRequest, 'pathParams'>,
      options?: { onSuccess?: () => void }
    ) =>
      addMutation.mutate(
        { pathParams: { departmentId: departmentId.toString() }, ...data },
        { onSuccess: () => options?.onSuccess?.() }
      ),
    isPending: addMutation.isPending,
  };
}

// ---------------------------------------------------------------------------
// Delete Mutation Template
export function useDeleteUser() {
  const createServiceMutation = useHostServiceMutation();
  const deleteMutation = createServiceMutation<DeleteResponse, DeleteRequest>(
    UserService.DeleteUser,
  );

  return {
    remove: (
      userId: number,
      justification: string,
      options?: { onSuccess?: () => void }
    ) =>
      deleteMutation.mutate(
        { pathParams: { userId: userId.toString() }, justification },
        { onSuccess: () => options?.onSuccess?.() }
      ),
    isPending: deleteMutation.isPending,
  };
}

// ---------------------------------------------------------------------------
// Logic Hook Template (Page State)
export const useUsersLogic = () => {
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState(1);
  const [deleteModal, setDeleteModal] = useState<{
    open: boolean;
    user: UserListItem | null;
  }>({ open: false, user: null });

  const { data: usersData, refetch } = useUsers({ page: currentPage, pageSize: 10 });
  const { remove, isPending } = useDeleteUser();

  const users = usersData?.data.items || [];

  const handleEdit = (userId: number) => {
    navigate(`/users/${userId}/edit`);
  };

  const handleDelete = (justification: string) => {
    if (deleteModal.user) {
      remove(deleteModal.user.userId, justification, {
        onSuccess: () => {
          refetch();
          setDeleteModal({ open: false, user: null });
        }
      });
    }
  };

  return {
    users,
    currentPage,
    setCurrentPage,
    deleteModal,
    setDeleteModal,
    isPending,
    handleEdit,
    handleDelete,
  };
};

// ---------------------------------------------------------------------------
// Filter State Hook
export const useFilters = <T extends Record<string, unknown>>(initialFilters: T) => {
  const [filters, setFilters] = useState<T>(initialFilters);

  const updateFilter = (key: keyof T, value: unknown) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }));
  };

  const resetFilters = () => {
    setFilters(initialFilters);
  };

  return { filters, setFilters, updateFilter, resetFilters };
};
