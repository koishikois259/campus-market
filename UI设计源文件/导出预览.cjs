// Rasterize the SVG design assets. This does not operate Pixso or a live browser.
// Usage: node 导出预览.cjs [directory containing the sharp package]
const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');
const sourceRoot = __dirname;
const root = path.dirname(sourceRoot);
const requireLibrary = process.argv[2]
  ? createRequire(path.join(process.argv[2], '__ui_dependencies__.cjs'))
  : require;
const sharp = requireLibrary('sharp');
const manifest = JSON.parse(fs.readFileSync(path.join(sourceRoot, '初稿_v0.1', '画板清单.json'), 'utf8'));

(async () => {
  for (const page of manifest.pages) {
    const target = path.join(root, page.png);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    await sharp(path.join(root, page.svg), { density: 144 }).png().toFile(target);
    const meta = await sharp(target).metadata();
    if (meta.width !== page.width * 2 || meta.height !== page.height * 2) {
      throw new Error(`Unexpected export dimensions for ${page.id}: ${meta.width}x${meta.height}`);
    }
    console.log(`${page.id}: ${meta.width}x${meta.height}`);
  }
})();
