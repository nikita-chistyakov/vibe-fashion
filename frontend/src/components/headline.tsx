import { APP_NAME } from '@/constants';

export const Headline = () => {
  return (
    <div className="p-4 text-lg text-gray-700">
      <p>
        <strong>{APP_NAME}</strong> helps you choose the perfect outfit!
      </p>
      <p>
        Whether you&apos;re unsure what to wear or want style suggestions, just
        ask and get personalized fashion advice.{' '}
      </p>
      <p>
        Need ideas for a Halloween costume? Fashion AI can help you find the
        most creative and fun looks for the holiday!
      </p>
    </div>
  );
};
