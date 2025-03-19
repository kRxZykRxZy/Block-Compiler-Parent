# CodeTorch Block Compiler Parent

Welcome to the **CodeTorch Block Compiler Parent** repository! This serves as the primary backend and shell for running a fully self-contained CodeTorch Block Compiler.

## Repository Structure

To transform this backend into a complete CodeTorch Block Compiler, you'll need the following repositories:

- **[CodeTorch Block Compiler Parent](https://github.com/CodeTorchNET/Block-Compiler-Parent)** *(This Repository)* — The main backend for CodeTorch Block Compiler.
- **[CodeTorch Block Compiler](https://github.com/CodeTorchNET/CodeTorch-Block-Compiler)** *(Required)* — The frontend repository based on a modified `turbowarp-gui`.
- **[scratch-vm](https://github.com/CodeTorchNET/scratch-vm)** *(Optional but Recommended)* — A modified `scratch-vm` repository that is the actual engine behind the compiler.
- **[scratch-blocks](https://github.com/CodeTorchNET/scratch-blocks)** *(Required for AI Tools)* — contains the block definitions for the compiler.
- **[scratch-storage](https://github.com/CodeTorchNET/scratch-storage)** — Handles project storage.

### Additional (Optional) Repositories
These are only necessary if the default versions experience issues:

- [scratch-render](https://github.com/CodeTorchNET/scratch-render)
- [scratch-svg-renderer](https://github.com/CodeTorchNET/scratch-svg-renderer)
- [scratch-paint](https://github.com/CodeTorchNET/scratch-paint)
- [scratch-parser](https://github.com/CodeTorchNET/scratch-parser)
- [scratch-audio](https://github.com/CodeTorchNET/scratch-audio)

## Requirements
Ensure you have the following installed:
- Docker
- Node.js (v18 or higher (v22 recommended), v16 as a fallback)

## Installation Guide

### Step 1: Clone the Backend Repository
```bash
git clone https://github.com/CodeTorchNET/Block-Compiler-Parent
cd Block-Compiler-Parent
```

### Step 2: Configure Environment Variables
- Rename `example.env` to `.env`
- Set your desired `MYSQL_ROOT_PASSWORD` and `InternalAPIKey`

### Step 3: Start Docker Containers
```bash
docker compose up -d
```
- The backend server will run at `http://localhost:{HOST_MACHINE_UNSECURE_HOST_PORT}`
- Visiting the URL should display `CodeTorch Block Compiler API is running.`

### Step 4: Install the Compiler
```bash
cd ..
git clone https://github.com/CodeTorchNET/CodeTorch-Block-Compiler
cd CodeTorch-Block-Compiler
npm ci
```
- Optionally modify `src/lib/brand.js` for branding changes.

### Step 5: Run or Build the Compiler
To run the compiler in development mode:
```bash
PORT=1154 npm start
```
- Accessible at `http://localhost:1154`

To build the compiler for production:
```bash
# macOS/Linux
NODE_ENV=production npm run build

# Windows (Command Prompt)
set NODE_ENV=production
npm run build

# Windows (PowerShell)
$env:NODE_ENV="production"
npm run build
```
- The compiled output will be available in the `build` directory.

### Step 6: Integrate with the Backend
- Copy the `build` folder to `Block-Compiler-Parent/src/static`
- Access the compiler at:
  ```
  http://localhost:{HOST_MACHINE_UNSECURE_HOST_PORT}/build/editor.html
  ```
  You should `Invalid Embed`, which is expected since it is designed to run within an iframe.

### Step 7: Build the Extensions Library
1. Clone the `turbowarp-extensions` repository:
   ```bash
   git clone https://github.com/turbowarp/extensions
    ```
2. Copy the `extensions` and `images` folders to `Block-Compiler-Parent/src/static/extensions`
3. Go to `https://extensions.turbowarp.org/generated-metadata/extensions-v0.json` and save the JSON file as `extensions.json` in the `Block-Compiler-Parent/src/static/extensions` folder.

## Using the Compiler in an Iframe
The `Block Compiler` is intended to be embedded within an iframe. If you see the `Invalid Embed` message, it indicates that the compiler is not currently running in an iframe.  

To resolve this, simply embed the compiler using an iframe. The base URL for the iframe is:  
`http://localhost:{HOST_MACHINE_UNSECURE_HOST_PORT}/build/`  

The compiler offers multiple pages, each designed for specific purposes:

- `/editor.html` — Main editor
- `/index.html` — Main window
- `/embed.html` — Embeddable version
- `/addons.html` — Add-ons management
- `/fullscreen.html` — Fullscreen mode

### URL Parameters
- `?onlyEditor=0|1` — Disables community functions if set to `1`
- `?new_project=0|1` — Creates a new project if set to `1`
- `?username={string}` — Sets the username for the new project
- `?token={string}` — Provides user authentication token
- `#{string}` — Specifies the project ID to load

## Internal API
The Internal API manages projects and user authentication. All requests must include the `InternalAPIKey` as a `token` parameter.

### Endpoints
- `POST /internal/updateProjectTitle` — Update project title
  - Parameters: `projectID` (int), `title` (string)
- `POST /internal/updateUserAuthToken` — Update or create user authentication tokens
  - Parameters: `user_id` (string), `usertoken` (string), `tokenExpiration` (timestamp)
- `POST /internal/updateProjectStatus` — Update project sharing status
  - Parameters: `projectID` (int), `shared` (bool)

## PostMessage Communication
The CodeTorch Block Compiler communicates with the parent window using `postMessage`. It supports the following messages, with the `type` always set to `block-compiler-action`:

- `communityPage` — Opens the community page
- `addonsPage` — Opens the add-ons page
- `doneCreatingProject` — Signals project creation completion
- `resizedStage` — Notifies parent of stage resize
- `createdRemix`- Notifies parent of a remix creation

## Why CodeTorch is Not Fully Open Source
Although the TurboWarp versions of `scratch-gui` and `scratch-vm` are licensed under GPL-3.0 (and this Block Compiler is a derivative of these works), CodeTorch is not fully open source. This is because of how CodeTorch and the CodeTorch Block Compiler are structured—they function as two separate programs, essentially keeping them at "arm's length." This setup is similar to using a GPL-3.0-licensed Software-as-a-Service (SaaS) tool, where the GPL-3.0 license applies only to the SaaS itself, not to third-party users. As a result, the rest of CodeTorch is considered a mere aggregation of the Compiler (which in this case is the `SaaS`) and is not subject to the GPL-3.0 license.


For more details on this, you can read the official GPL-3.0 guidelines on the following topics: [Mere Aggregation](https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation), [GPL Plugins](https://www.gnu.org/licenses/gpl-faq.en.html#GPLPlugins), and [GPL in Proprietary Systems](https://www.gnu.org/licenses/gpl-faq.en.html#GPLInProprietarySystem).

If you have any questions or concerns about this (or just think I'm wrong), please feel free to contact me at [codetorch@codetorch.net](mailto:codetorch@codetorch.net). (Trust me, I'm just a teenager in high school who's doing this for fun, so I'm not trying to do anything to get myself in trouble.)