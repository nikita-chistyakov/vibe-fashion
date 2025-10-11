import { create } from 'zustand';
import { Roles } from '@/constants';
import { Image } from '@/types';

const defaultImages = [
  {
    base64: 'data:image/png;base64,1234567890',
    description: 'Image description',
  },
  {
    base64: 'data:image/png;base64,1234567890',
    description: 'Image description',
  },
  {
    base64: 'data:image/png;base64,1234567890',
    description:
      'Image description Image description Image description Image description Image description Image description',
  },
];

const defaultMessages = [
  {
    role: Roles.ASSISTANT,
    content: 'Hello, how can I help you today?',
  },
  {
    role: Roles.USER,
    content: 'I have a question about the weather in Tokyo.',
  },
  {
    role: Roles.ASSISTANT,
    content: 'Hello, how can I help you today?',
  },
  {
    role: Roles.USER,
    content: 'I have a question about the weather in Tokyo.',
  },
  {
    role: Roles.ASSISTANT,
    content: 'Hello, how can I help you today?',
  },
  {
    role: Roles.USER,
    content: 'I have a question about the weather in Tokyo.',
  },
  {
    role: Roles.ASSISTANT,
    content: 'Hello, how can I help you today?',
  },
  {
    role: Roles.USER,
    content: 'I have a question about the weather in Tokyo.',
  },
] as Msg[];

export interface Msg {
  role: typeof Roles.ASSISTANT | typeof Roles.USER;
  content: string;
}

interface ConversationState {
  conversation: Msg[];
  addMessages: (messages: Msg[]) => void;
  imagesStored: Image[];
  addImagesStored: (images: Image[]) => void;
  removeAllMessages: () => void;
}

export const useConversationStore = create<ConversationState>((set) => ({
  // conversation: defaultMessages,
  // imagesStored: defaultImages,
  conversation: [] as Msg[],
  imagesStored: [] as Image[],
  addImagesStored: (images: Image[]) =>
    set((state: { imagesStored: Image[] }) => ({
      imagesStored: [...state.imagesStored, ...images],
    })),
  addMessages: (messages: Msg[]) =>
    set((state: { conversation: Msg[] }) => ({
      conversation: [...state.conversation, ...messages],
    })),
  removeAllMessages: () => set({ conversation: [] }),
}));
