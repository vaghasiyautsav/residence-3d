# Skills

Playbooks for building and maintaining 3D house models from architectural drawings, written so the method can be reused on other projects.

- [`house-plans-to-3d`](house-plans-to-3d/SKILL.md): the general method. It covers:
  - reading working drawings (calibration, written versus scaled dimensions, elevations, roof, site and survey);
  - building an accurate three.js model;
  - real-size interiors, site and street context;
  - PIN-locked deploy and QA.

  Its `scripts/` folder holds:
  - `pdf_probe.py`: reads any drawing sheet in plan millimetres;
  - `wall_coverage.py`: checks that every drawn wall exists in the model.
- [`vaghasiya-residence-3d`](vaghasiya-residence-3d/SKILL.md): the project-specific facts and workflow for this house.

To use one with a coding agent that supports skills, copy its folder into the agent's skills directory (for example `~/.claude/skills/`). The scripts need Python 3 and PyMuPDF (`pip install pymupdf`).
