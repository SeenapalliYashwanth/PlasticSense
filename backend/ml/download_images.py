from icrawler.builtin import BingImageCrawler

def crawl_images(folder, keyword, max_num=50):
    crawler = BingImageCrawler(storage={'root_dir': folder})
    try:
        crawler.crawl(keyword=keyword, max_num=max_num)
    except Exception as e:
        print(f"[ERROR] Failed to crawl '{keyword}' into '{folder}': {e}")

# Download PET images
crawl_images('dataset/PET', 'PET plastic bottle', max_num=50)

# Download HDPE images
crawl_images('dataset/HDPE', 'HDPE plastic container', max_num=50)

# Download PVC images
crawl_images('dataset/PVC', 'PVC plastic pipe', max_num=50)