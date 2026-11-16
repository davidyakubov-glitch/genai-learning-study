"""Two figures for synthetic learning-study data; error bars are sample SD."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from process_data import ROOT, run

GROUPS = ['traditional', 'genai']
COLORS = ['#0072B2', '#D55E00']


def create_figures(rows, aggregates):
    destination = ROOT / 'reports/figures'
    destination.mkdir(parents=True, exist_ok=True)
    paths = []
    labels = [f'{label}\n(n = {sum(r["group"] == group for r in rows)})'
              for label, group in zip(['Traditional', 'Structured GenAI'], GROUPS)]
    for name, metric, title, ylabel, limits, caption in [
        ('fig1_learning_gain', 'learning_gain_percentage_points',
         'Learning gain by learning method', 'Post-test minus pre-test (percentage points)', (-2, 25),
         'Figure 1. Points: synthetic records; black markers: means; error bars: +/-1 sample SD.'),
        ('fig2_task_time', 'task_minutes',
         'Practice-task time by learning method', 'Recorded practice-task time (minutes)', (0, 42),
         'Figure 2. Points: synthetic records; black markers: means; error bars: +/-1 sample SD.')]:
        fig, ax = plt.subplots(figsize=(8, 5.4))
        for x, group in enumerate(GROUPS):
            values = [r[metric] for r in rows if r['group'] == group]
            positions = [x + (j - (len(values)-1)/2)*0.055 for j in range(len(values))]
            ax.scatter(positions, values, color=COLORS[x], marker=['o', '^'][x], s=45, zorder=3)
            stats = next(a for a in aggregates if a['group'] == group and a['metric'] == metric)
            ax.errorbar(x + .25, stats['mean'], yerr=stats['sd'], fmt='s',
                        color='black', capsize=6, markersize=6, zorder=4)
        if metric == 'task_minutes':
            ax.axhline(40, color='0.4', linestyle='--', linewidth=1)
            ax.text(.5, 40.5, '40-minute task cap', ha='center', fontsize=9)
        ax.set(xticks=[0, 1], xticklabels=labels, xlim=(-.45, 1.55), ylim=limits,
               xlabel='Learning method', ylabel=ylabel, title=title)
        ax.grid(axis='y', color='0.9')
        ax.set_axisbelow(True)
        ax.spines[['top', 'right']].set_visible(False)
        fig.suptitle('SYNTHETIC DEMONSTRATION — NOT EXPERIMENTAL EVIDENCE', fontsize=10, fontweight='bold')
        fig.text(.5, .035, caption + '\nSD shows fixture dispersion, not uncertainty about a real population.',
                 ha='center', fontsize=9)
        fig.tight_layout(rect=(0, .11, 1, .94))
        for ext in ['png', 'pdf']:
            path = destination / f'{name}.{ext}'
            fig.savefig(path, dpi=300)
            paths.append(path)
        plt.close(fig)
    return paths


if __name__ == '__main__':
    rows, aggregates, _ = run()
    print('\n'.join(str(p) for p in create_figures(rows, aggregates)))
