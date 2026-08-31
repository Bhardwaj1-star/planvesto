import { pages } from "../lib/pages";
export default function HomePage() {
  return <div dangerouslySetInnerHTML={{ __html: pages["/"].body }} />;
}
