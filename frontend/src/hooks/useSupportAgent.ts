import { useMutation } from '@tanstack/react-query';
import { analyze } from '../services/api';

export const useSupportAgent = () => useMutation({ mutationFn: analyze });
