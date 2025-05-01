declare module '@heroui/spinner' {
    import React from 'react';
  
    export interface SpinnerProps {
      size?: 'sm' | 'md' | 'lg';
      color?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger';
      labelText?: string;
      className?: string;
      style?: React.CSSProperties;
    }
  
    export const Spinner: React.FC<SpinnerProps>;
  }