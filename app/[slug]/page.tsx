import { notFound } from "next/navigation";
import { pages } from "../../lib/pages";

export function generateStaticParams() {
  return Object.keys(pages).filter((slug) => slug !== "/").map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return { title: pages[slug as keyof typeof pages]?.title ?? "Planvesto" };
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const page = pages[slug as keyof typeof pages];
  if (!page) notFound();
  return <div dangerouslySetInnerHTML={{ __html: page.body }} />;
}
