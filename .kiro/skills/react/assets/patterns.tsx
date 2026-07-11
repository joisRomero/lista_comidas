import { Modal, Descriptions } from 'antd';
import type { ModalProps, DescriptionsProps } from 'antd';
import { forwardRef, useState } from 'react';
import styles from './Component.module.css';

export interface AntaModalProps extends ModalProps {}

export const AntaModal = ({ className, ...props }: AntaModalProps) => {
  return (
    <Modal 
      className={`${styles.modal} ${className ?? ''}`}
      {...props} 
    />
  );
};

const { Item } = Descriptions;

interface AntaDescriptionsProps extends DescriptionsProps {}

const AntaDescriptionsBase = forwardRef<HTMLDivElement, AntaDescriptionsProps>(
  ({ className, ...props }, _ref) => (
    <Descriptions className={`${styles.descriptions} ${className ?? ''}`} {...props} />
  )
);

AntaDescriptionsBase.displayName = 'AntaDescriptions';

export const AntaDescriptions = Object.assign(AntaDescriptionsBase, { Item });

interface ItemType {
  id: number;
  name: string;
}

export const useModalState = <T extends ItemType>() => {
  const [modal, setModal] = useState<{ open: boolean; item: T | null }>({ 
    open: false, 
    item: null 
  });

  const open = (item: T) => setModal({ open: true, item });
  const close = () => setModal({ open: false, item: null });

  return { modal, open, close };
};

export const useConfirm = () => {
  const [modal, contextHolder] = Modal.useModal();
  
  const confirmDelete = (itemName: string, onConfirm: () => void) => {
    modal.confirm({
      title: 'Confirmar eliminacion',
      content: `¿Estas seguro de eliminar "${itemName}"?`,
      okText: 'Eliminar',
      okButtonProps: { danger: true },
      cancelText: 'Cancelar',
      onOk: onConfirm,
      centered: true,
    });
  };

  return { confirmDelete, contextHolder };
};

export const formatCurrency = (amount: number, currency: string) => {
  return `${currency} ${amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
};

export const formatDate = (date: string, locale = 'es-ES') => {
  return new Date(date).toLocaleDateString(locale, { 
    day: 'numeric', month: 'long', year: 'numeric' 
  });
};
