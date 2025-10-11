import { create } from 'zustand';

interface InputState {
  images: string[];
  setImages: (images: string[]) => void;
  text: string;
  setText: (text: string) => void;
}

export const useInputStore = create<InputState>((set) => ({
  images: [],
  setImages: (images: string[]) => set({ images }),
  text: '',
  setText: (text: string) => set({ text }),
}));
