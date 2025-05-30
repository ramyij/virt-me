import { useRouter } from 'next/router';

const projects = {
  'youtube-video': {
    title: 'YouTube Video + GitHub Repo',
    description: 'A project showcasing a YouTube video and its corresponding GitHub repository.',
    content: 'This project includes a YouTube video explaining the concept and a GitHub repository with the source code.',
    link: 'https://github.com/your-repo',
  },
  'podcast-guest': {
    title: 'Podcast Guest Appearance',
    description: 'Listen to my guest appearance on a podcast.',
    content: 'In this podcast, I discuss various topics related to my expertise.',
    link: 'https://podcast-url.com',
  },
  'demo-recording': {
    title: 'Demo Recording',
    description: 'A demo recording with my voiceover.',
    content: 'This is a demo recording where I explain the project in detail.',
    link: '/path-to-demo.mp4',
  },
  'sales-pitch': {
    title: 'Sales Pitch Video',
    description: 'A sales pitch video showcasing my skills.',
    content: 'This video demonstrates my ability to pitch ideas effectively.',
    link: '/path-to-sales-pitch.mp4',
  },
};

export default function ProjectDetail() {
  const router = useRouter();
  const { id } = router.query;
  const project = projects[id];

  if (!project) {
    return <p>Project not found.</p>;
  }

  return (
    <div>
      <h1>{project.title}</h1>
      <p>{project.description}</p>
      <p>{project.content}</p>
      <a href={project.link} target="_blank" rel="noopener noreferrer">Learn more</a>
    </div>
  );
}