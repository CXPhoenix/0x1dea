import { createContentLoader } from "vitepress";

export default createContentLoader('post/**/*.md', {
    includeSrc: true,
    render: false,
    excerpt: false,
    transform(rawData) {
        const postListData = rawData.map((post, idx) => {
            return {
                title: post.frontmatter?.title,
                abstract: post.frontmatter?.abstract ?? "閱讀更多...",
                createdTime: post.frontmatter?.createdTime ?? new Date(0 + idx * 1000),
                thumbnil: post.frontmatter?.thumbnil ?? `https://picsum.photos/seed/${new Date().getTime() + idx * 100}/400/300`,
                url: post.url,
                category: (() => {
                    // post.url usually comes as /post/path/to/file or /post/path/to/file.html

                    // Remove leading '/post/' and optional trailing extensions/slashes
                    const relativePath = post.url.replace(/^\/post\//, '').replace(/\.(md|html)$/, '').replace(/\/$/, '')
                    const segments = relativePath.split('/')

                    if (segments.length > 1) {
                        // Join all but the last segment (which is the post slug/filename)
                        return segments.slice(0, -1).join('-')
                    }
                    if (segments.length > 0) {
                        return segments[0]
                    }
                    return '綜合'
                })()
            }


        })
        return postListData
    }
});