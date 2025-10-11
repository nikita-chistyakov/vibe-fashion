export interface CapturedFrame {
  base64: string;
  timestampMs: number;
  width: number;
  height: number;
}

export async function getFrameFromStream(
  video: HTMLVideoElement,
  imageMimeType = 'image/png',
): Promise<CapturedFrame> {
  if (!video) throw new Error('No HTMLVideoElement provided.');

  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('No CanvasRenderingContext2D provided.');

  ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
  const dataUrl = canvas.toDataURL(imageMimeType);
  const base64 = dataUrl.split(',')[1];
  return {
    base64,
    timestampMs: Math.round(performance.now()),
    width: video.videoWidth,
    height: video.videoHeight,
  };
}
