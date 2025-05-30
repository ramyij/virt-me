import Link from 'next/link';

const projects = [
  {
    id: 'youtube-video',
    title: 'YouTube Video + GitHub Repo',
    description: 'A project showcasing a YouTube video and its corresponding GitHub repository.',
    link: 'https://github.com/your-repo',
    type: 'video',
  },
  {
    id: 'podcast-guest',
    title: 'Podcast Guest Appearance',
    description: 'Listen to my guest appearance on a podcast.',
    link: 'https://podcast-url.com',
    type: 'podcast',
  },
  {
    id: 'demo-recording',
    title: 'Demo Recording',
    description: 'A demo recording with my voiceover.',
    link: '/path-to-demo.mp4',
    type: 'video',
  },
  {
    id: 'sales-pitch',
    title: 'Sales Pitch Video',
    description: 'A sales pitch video showcasing my skills.',
    link: '/path-to-sales-pitch.mp4',
    type: 'video',
  },
];

export default function Portfolio() {
  return (
    <div>
      <h1>Portfolio</h1>
      <ul>
        {projects.map((project) => (
          <li key={project.id}>
            <Link href={`/portfolio/${project.id}`}>
              <h2>{project.title}</h2>
              <p>{project.description}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}