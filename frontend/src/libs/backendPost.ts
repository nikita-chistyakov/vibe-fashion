import { backendPostResponse } from '@/types';

const base = process.env.NEXT_PUBLIC_BASE_URL!;

interface backendPostProps {
  text: string;
  imageBase64: string;
}

export const backendPost = async ({ text, imageBase64 }: backendPostProps) => {
  try {
    const response = await fetch(`${base}/fashion-workflow`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: text, base64_image: imageBase64 }),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch');
    }
    return response.json() as Promise<backendPostResponse>;
  } catch (error) {
    console.log('error', error);
    return {
      text: 'Error from server',
      images: [],
      success: false,
      error_message: 'Error from server',
    };
  }
};
