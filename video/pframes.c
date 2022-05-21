/*
 * Copyright (c) 2012 Stefano Sabatini
 * Copyright (c) 2014 Clément Bœsch
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include <math.h>
#include <libavutil/motion_vector.h>
#include <libavformat/avformat.h>

/*
build command: gcc pframes.c -g -o pframes -I /usr/local/include -L /usr/local/lib -lavformat -lavutil -lavcodec -lm -std=c99

usage: 
./pframes -i {video_path} -ss {start_second} -t {duration} -vframes {max_frames_count}

example：

Gets the all frame type of each second from 10 to 30 seconds:
./pframes -i a.mp4 -ss 10 -t 20

*/

static AVFormatContext *fmt_ctx = NULL;
static AVCodecContext *video_dec_ctx = NULL;
static AVStream *video_stream = NULL;
static const char *src_filename = NULL;

static int video_stream_idx = -1;
static AVFrame *frame = NULL;
static int video_frame_count = 0;

static int64_t start_sec = 0;
static int64_t end_sec = INT64_MAX;
static int end_flag = 0;
static char frame_char_type = 'a';
static int max_frames_count = -1;
static int nb_f = 0;


static int extract_frames(const AVPacket *pkt)
{
    int ret = avcodec_send_packet(video_dec_ctx, pkt);
    if (ret < 0) {
        fprintf(stderr, "Error while sending a packet to the decoder: %s\n", av_err2str(ret));
        return ret;
    }

    while (ret >= 0)  {
        ret = avcodec_receive_frame(video_dec_ctx, frame);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
            break;
        } else if (ret < 0) {
            fprintf(stderr, "Error while receiving a frame from the decoder: %s\n", av_err2str(ret));
            return ret;
        }
        // printf("frame_number=%d\n", video_dec_ctx->frame_number);
        

        if (ret >= 0) {
            int i;
            AVFrameSideData *sd;
        nb_f++;

            int current_pts_sec = frame->pts * av_q2d(video_stream->time_base);
            // printf("cur=%d\n", current_pts_sec);
            if (current_pts_sec < start_sec) continue;
            if (current_pts_sec > end_sec) {
                end_flag = 1;
                break;
            }

            video_frame_count++;
            if (frame->pict_type == 0){
                frame_char_type = '*';
            } else if (frame->pict_type == 1) {
                frame_char_type = 'I';
            } else if (frame->pict_type == 2) {
                frame_char_type = 'P';
            } else if (frame->pict_type == 3) {
                frame_char_type = 'B';
            } else if (frame->pict_type == 4) {
                frame_char_type = 'S';
            }
            printf("%d,%d,%c\n",video_frame_count, current_pts_sec, frame_char_type);
            av_frame_unref(frame);
            if (max_frames_count >0 && video_frame_count >= max_frames_count){
                end_flag = 1;
                break;
            }
        }else{
            printf("ret = %d, %d\n", ret, frame->pict_type);
        }
    }

    return 0;
}

static int open_codec_context(AVFormatContext *fmt_ctx, enum AVMediaType type)
{
    int ret;
    AVStream *st;
    AVCodecContext *dec_ctx = NULL;
    AVCodec *dec = NULL;
    AVDictionary *opts = NULL;

    ret = av_find_best_stream(fmt_ctx, type, -1, -1, &dec, 0);
    if (ret < 0) {
        fprintf(stderr, "Could not find %s stream in input file '%s'\n",
                av_get_media_type_string(type), src_filename);
        return ret;
    } else {
        int stream_idx = ret;
        st = fmt_ctx->streams[stream_idx];

        dec_ctx = avcodec_alloc_context3(dec);
        if (!dec_ctx) {
            fprintf(stderr, "Failed to allocate codec\n");
            return AVERROR(EINVAL);
        }

        ret = avcodec_parameters_to_context(dec_ctx, st->codecpar);
        if (ret < 0) {
            fprintf(stderr, "Failed to copy codec parameters to codec context\n");
            return ret;
        }

        /* Init the video decoder */
        av_dict_set(&opts, "flags2", "+export_mvs", 0);
        if ((ret = avcodec_open2(dec_ctx, dec, &opts)) < 0) {
            fprintf(stderr, "Failed to open %s codec\n",
                    av_get_media_type_string(type));
            return ret;
        }

        video_stream_idx = stream_idx;
        video_stream = fmt_ctx->streams[video_stream_idx];
        video_dec_ctx = dec_ctx;
    }

    return 0;
}

int main(int argc, char **argv)
{
    int ret = 0;
    AVPacket pkt = { 0 };
    int64_t t_sec = 0;

    // src_filename = argv[1];
    for (int i = 1; i < argc; i++)
    {
        // printf("argc i : %d, %s\n", i, argv[i]);
        if (strcmp(argv[i],"-i") == 0)
        {
            i++;
            src_filename = argv[i];
        }else if (strcmp(argv[i],"-ss") == 0)
        {
            i++;
            start_sec = atoi(argv[i]);
        }
        else if (strcmp(argv[i],"-t") == 0)
        {
            i++;
            t_sec = atoi(argv[i]);
        }
        else if (strcmp(argv[i],"-vframes") == 0)
        {
            i++;
            max_frames_count = atoi(argv[i]);
        }
        
    }

    if (avformat_open_input(&fmt_ctx, src_filename, NULL, NULL) < 0) {
        fprintf(stderr, "Could not open source file %s\n", src_filename);
        exit(1);
    }

    if (avformat_find_stream_info(fmt_ctx, NULL) < 0) {
        fprintf(stderr, "Could not find stream information\n");
        exit(1);
    }

    open_codec_context(fmt_ctx, AVMEDIA_TYPE_VIDEO);
    av_dump_format(fmt_ctx, 0, src_filename, 0);

    if (t_sec){
        end_sec = start_sec + t_sec - 1;
    }
    // else {
    //     end_sec = video_stream->duration;
    // }

    int64_t start_timestamp = start_sec/av_q2d(video_stream->time_base);

    // AVSEEK_FLAG_BACKWARD = 1

    if (start_sec && av_seek_frame(fmt_ctx, video_stream_idx, start_timestamp, 1) < 0){
        fprintf(stderr, "Could not seek start_sec to %lld\n", start_sec);
        exit(1);
    }

    if (!video_stream) {
        fprintf(stderr, "Could not find video stream in the input, aborting\n");
        ret = 1;
        goto end;
    }

    frame = av_frame_alloc();
    if (!frame) {
        fprintf(stderr, "Could not allocate frame\n");
        ret = AVERROR(ENOMEM);
        goto end;
    }
    int nb_pkt = 0;
    /* read frames from the file */
    while (av_read_frame(fmt_ctx, &pkt) >= 0) {
        if (end_flag == 1) break;
        if (pkt.stream_index == video_stream_idx ){
            ret = extract_frames(&pkt);
        }
        av_packet_unref(&pkt);
        nb_pkt++;

        if (ret < 0)
            break;
    }
    printf("nb_pkt=%d\n", nb_pkt);
    printf("nb_f=%d\n", nb_f);


    /* flush cached frames */
    // extract_all_mvs(NULL);

end:
    avcodec_free_context(&video_dec_ctx);
    avformat_close_input(&fmt_ctx);
    av_frame_free(&frame);
    return ret < 0;
}
