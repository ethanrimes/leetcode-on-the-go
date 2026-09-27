# Pattern Atlas — LeetCode on the go

A study-first monorepo for recognizing algorithmic patterns, recalling their invariants, drafting solutions, and reviewing canonical implementations.

- `apps/web`: React + TypeScript, responsive browser study workspace.
- `apps/ios`: native SwiftUI iPhone/iPad app, with an offline curriculum.
- `packages/content`: versioned curriculum shared by both apps.
- `packages/core`: typed curriculum queries and review scheduling.
- `scripts`: content authoring, validation, and resource generation.
- `infrastructure`: Azure hosting and repeatable deployment.

## Development

Requires Node 22.12+, Python 3.10+, and npm. iOS additionally requires Xcode 16+ and XcodeGen.

```sh
npm install
npm run build
npm run dev
npm test
npm run test:e2e
npm run ios:generate
open apps/ios/PatternAtlas.xcodeproj
```

Study progress and code drafts stay on the current device. Export/import is provided for backups and moving progress between devices. Running code and submitting solutions happen on LeetCode.

## Curriculum approach

Organize knowledge as topic → technique family → subfamily → individual pattern. Each node has an approach and teaching guidance; each leaf connects to worked problem cards. Difficulty of a problem is separate from the learning level and priority of its pattern. Problems may demonstrate more than one pattern.

Original summaries, explanations, and code are authored for this project. LeetCode titles, IDs, difficulty, and URLs are reference metadata. No paid editorials or hidden test cases are included. See `docs/SOURCES.md` for reference methodology and coverage boundaries.

This project is independent of LeetCode, EndlessCheng, and labuladong.
