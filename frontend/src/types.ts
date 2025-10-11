export interface Image {
  base64?: string;
  description?: string;
  subtennatilityScore?: number;
}

export interface backendPostResponse {
  text: string;
  images: Image[];
  success: boolean;
  error_message: string | null;
}
