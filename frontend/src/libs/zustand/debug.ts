import { create } from 'zustand';

interface DebugState {
  isDebugOpen: boolean;
  triggerDebugOpen: () => void;
}

export const useDebugStore = create<DebugState>((set) => ({
  isDebugOpen: false,
  triggerDebugOpen: () =>
    set((state: DebugState) => ({
      isDebugOpen: !state.isDebugOpen,
    })),
}));
