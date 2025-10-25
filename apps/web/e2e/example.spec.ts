import { test, expect } from "@playwright/test";

test("homepage renders", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await expect(page.getByText("Tetris Game Roulette")).toBeVisible();
});
