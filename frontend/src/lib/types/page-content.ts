export type PageContent = {
  title: string;
  description: string;
  stats: Array<{ title: string; value: string; description: string }>;
  sections: Array<{ title: string; body: string; items?: string[] }>;
};
